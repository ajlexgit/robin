from django.db import models
from django.conf import settings
from django.utils.timezone import now
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.db.models.functions import Coalesce, Value
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from mptt.managers import TreeManager
from libs.aliased_queryset import AliasedQuerySetMixin
from . import options


class CommentQuerySet(AliasedQuerySetMixin, models.QuerySet):
    def aliases(self, qs, kwargs):
        # entity
        entity = kwargs.pop('entity', None)
        if entity is not None:
            content_type = ContentType.objects.get_for_model(type(entity))
            qs &= models.Q(content_type=content_type.pk, object_id=entity.pk)

        # visible
        visible = kwargs.pop('visible', None)
        if visible is not None:
            qs &= models.Q(visible=bool(visible))

        return qs

    def only(self, *fields):
        """ Fix for MPTT """
        mptt_meta = self.model._mptt_meta
        mptt_fields = tuple(
            getattr(mptt_meta, key)
            for key in ('left_attr', 'right_attr', 'tree_id_attr', 'level_attr')
        )
        final_fields = set(mptt_fields + fields + tuple(mptt_meta.order_insertion_by))
        return super().only(*final_fields)

    def with_permissions(self, user):
        """ Генератор с полями прав на коммент """
        for comment in self:
            comment.add_permissions(user)
            yield comment


class CommentTreeManager(TreeManager):
    _queryset_class = CommentQuerySet

    def get_for(self, entity, visible=True):
        """ Получение комментариев к сущности """
        return self.filter(
            entity=entity,
            visible=visible,
        ).select_related('user__pk', 'user__username', 'user__avatar')


class Comment(MPTTModel):
    """ Модель комментария """
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    entity = generic.GenericForeignKey()

    parent = TreeForeignKey('self', blank=True, null=True, verbose_name=_('parent comment'))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comments', editable=False, verbose_name=_('author'))
    text = models.TextField(_('text'), max_length=options.COMMENT_MAX_LENGTH)
    rating = models.IntegerField(_('rating'), default=0, editable=False)

    created = models.DateTimeField(_('created on'), editable=False)
    deleted = models.BooleanField(_('deleted'), default=False, editable=False)
    deleted_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, editable=False,
                                   related_name='+', verbose_name=_('deleted by'))
    visible = models.BooleanField(_('visible'), default=True, editable=False)
    sort_order = models.PositiveIntegerField(_('sort order'), default=0, editable=False)

    objects = CommentTreeManager()

    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = _('comments')
        permissions = (
            ('can_reply', 'Can reply on comment'),
            ('can_post', 'Can post comment'),
            ('can_edit', 'Can edit comment'),
            ('can_delete', 'Can delete comment'),
            ('can_vote', 'Can vote for comment'),
        )

    class MPTTMeta:
        order_insertion_by = ['sort_order']

    def __str__(self):
        return 'Comment(%r)' % self.short_text

    @property
    def short_text(self):
        return '{}...'.format(self.text[:80]) if len(self.text) > 80 else self.text

    @property
    def final_level(self):
        return min(self.get_level(), options.MAX_LEVEL)

    def save(self, *args, **kwargs):
        is_add = not self.pk
        if is_add:
            self.created = now()

            sort_order = self.get_siblings().aggregate(
                max=models.Max('sort_order')
            ).get('max')
            self.sort_order = 0 if sort_order is None else sort_order + 1
        else:
            # Обновляем видимость
            visible_descendants = self.get_descendants().filter(deleted=False)
            if visible_descendants.exists():
                self.visible = True
            else:
                self.visible = not self.deleted

        super().save(*args, **kwargs)

        if is_add:
            # Изменение родителя запрещено, поэтому обновляем дерево
            # только при добавлении
            Comment.objects.partial_rebuild(self.tree_id)
        else:
            # Обновляем видимость родителей
            self.update_parent_visibility()

    def update_parent_visibility(self):
        """
        Если текущий комментарий видимый - делаем всех родителей видимыми.
        Если текущий комментарий невидим и у него нет видимых соседей -
        обновляем видимость родителя и преверяем его родителя.
        """
        if not self.parent:
            return
        elif self.visible:
            self.get_ancestors().update(visible=True)
        else:
            # Скрываем родителя через SQL, чтобы избавиться от рекурсии в save()
            parent = Comment.objects.filter(pk=self.parent.pk).only('parent', 'deleted', 'visible').select_related('parent__deleted')
            parent.update(visible=not self.parent.deleted)
            parent.first().update_parent_visibility()

    def add_permissions(self, user):
        self.can_post = user.has_perm('comments.can_post')
        self.can_reply = user.has_perm('comments.can_reply', self)
        self.can_edit = user.has_perm('comments.can_edit', self)
        self.can_delete = user.has_perm('comments.can_delete', self)
        self.can_restore = user.has_perm('comments.can_restore', self)
        self.can_vote = user.has_perm('comments.can_vote', self)

    def has_childs(self):
        childs = Comment.objects.filter(position__startswith=self.position)
        return childs.count() > 1


class CommentVote(models.Model):
    """ Рейтинг комментария """
    comment = models.ForeignKey(Comment, related_name='votes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comment_votes')
    value = models.SmallIntegerField(choices=((1, '+1'), (-1, '-1')))

    class Meta:
        verbose_name = _('vote')
        verbose_name_plural = _('votes')
        unique_together = ('comment', 'user')

    def __str__(self):
        return 'CommentVote(%+d for comment %d)' % (self.value, self.comment.pk)

    def update(self):
        self.comment.rating = self.comment.votes.aggregate(
            rating=Coalesce(models.Sum('value'), Value(0))
        )['rating']
        self.comment.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.update()
