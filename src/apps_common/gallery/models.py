import os
from django.db import models
from django.core import checks
from django.conf import settings
from django.utils.timezone import now
from django.contrib.contenttypes import generic
from django.core.exceptions import ValidationError
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from model_utils.managers import InheritanceQuerySetMixin
from libs.variation_field import *
from libs.videolink_field import VideoLinkField
from libs.media_storage import MediaStorage
from libs.aliased_queryset import AliasedQuerySetMixin
from libs.upload import upload_file, URLError
from .fields import GalleryImageField, GalleryVideoLinkPreviewField

__all__ = ('GalleryBase', 'GalleryItemBase', 'GalleryImageItem', 'GalleryVideoLinkItem')


MAX_SIZE_DEFAULT = getattr(settings,  'GALLERY_MAX_SIZE_DEFAULT', 12*1024*1024)
MIN_DIMENSIONS_DEFAULT = getattr(settings,  'GALLERY_MIN_DIMENSIONS_DEFAULT', (0, 0))
MAX_DIMENSIONS_DEFAULT = getattr(settings,  'GALLERY_MAX_DIMENSIONS_DEFAULT', (6000, 6000))
MAX_SOURCE_DIMENSIONS_DEFAULT = getattr(settings,  'GALLERY_MAX_SOURCE_DIMENSIONS_DEFAULT', (2048, 2048))
ADMIN_CLIENT_RESIZE_DEFAULT = getattr(settings,  'GALLERY_ADMIN_CLIENT_RESIZE_DEFAULT', False)


class GalleryItemQuerySet(InheritanceQuerySetMixin, AliasedQuerySetMixin, models.QuerySet):
    """ QuerySet элемента галереи """
    def aliases(self, qs, kwargs):
        """ Добавляем возможность фильтровать по конктерной модели элемента """
        model = kwargs.pop('model', None)
        if model is not None:
            ct = ContentType.objects.get_for_model(model, for_concrete_model=False)
            qs &= models.Q(self_type=ct)
        return qs

    def _filter_or_exclude(self, *args, **kwargs):
        """ Возвращаем реальные классы элементов галерей при фильтрации """
        return super()._filter_or_exclude(*args, **kwargs).select_subclasses()


class GalleryItemBase(models.Model):
    """ Базовый класс элемента галереи """
    _cache = {}

    # Имена полей, чьи значения копируются при клонировании элемента
    COPY_FIELDS = set()

    self_type = models.ForeignKey(ContentType,
        editable=False, related_name='+',
        help_text="Для выборки элементов определенного типа")
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    gallery = generic.GenericForeignKey(for_concrete_model=False)
    description = models.TextField(_('description'), blank=True)

    sort_order = models.PositiveIntegerField(_('sort order'), default=0)
    created = models.DateTimeField(_('created on'))
    changed = models.DateTimeField(_('changed on'), auto_now=True)

    objects = GalleryItemQuerySet.as_manager()

    class Meta:
        verbose_name = _('gallery item')
        verbose_name_plural = _('gallery items')
        ordering = ('object_id', 'sort_order', 'created', )
        index_together = (('content_type', 'object_id'), )

    def save(self, *args, **kwargs):
        is_add = not self.pk
        if is_add:
            self.self_type = ContentType.objects.get_for_model(type(self), for_concrete_model=False)
            self.created = now()

            sort_order = self.gallery.items.aggregate(max=models.Max('sort_order')).get('max', 0)
            self.sort_order = 0 if sort_order is None else sort_order + 1

        super().save(*args, **kwargs)

    @classmethod
    def check(cls, **kwargs):
        errors = super().check(**kwargs)
        errors.extend(cls._check_copy_fields(**kwargs))
        return errors

    @classmethod
    def _check_copy_fields(cls, **kwargs):
        if not isinstance(cls.COPY_FIELDS, set):
            return [
                checks.Error(
                    'COPY_FIELDS should be an instance of set',
                    obj=cls
                )
            ]
        else:
            return []

    @property
    def is_image(self):
        return isinstance(self, GalleryImageItem)

    @property
    def is_video_link(self):
        return isinstance(self, GalleryVideoLinkItem)

    def after_copy(self, **kwargs):
        """
            Постобработка скопированного элемента.
            Параметр self - это уже новый элемент.
        """
        pass


def generate_filepath(instance, filename):
    """ Генерация пути сохранения файла """
    return instance.generate_filename(os.path.basename(filename))


class GalleryImageItem(GalleryItemBase):
    """ Элемент-картинка галереи """
    _cache = {}

    COPY_FIELDS = GalleryItemBase.COPY_FIELDS | {'image_crop', }

    # Корневая папка (storage)
    STORAGE_LOCATION = None

    # Границы размеров картинок, при превышении которых вызывается ошибка валидации
    MIN_DIMENSIONS = MIN_DIMENSIONS_DEFAULT
    MAX_DIMENSIONS = MAX_DIMENSIONS_DEFAULT

    # Приблизительный размер, к которому приводятся исходники картинок
    MAX_SOURCE_DIMENSIONS = MAX_SOURCE_DIMENSIONS_DEFAULT

    # Максимальный вес картинок
    MAX_SIZE = MAX_SIZE_DEFAULT

    # Уменьшать картинку до размера MAX_SOURCE_DIMENSIONS в админке на клиенте
    ADMIN_CLIENT_RESIZE = ADMIN_CLIENT_RESIZE_DEFAULT

    # Качество исходника в случае, когда он сохраняется через PIL
    SOURCE_QUALITY = 90

    # Качество картинок вариаций по умолчанию
    DEFAULT_QUALITY = 85

    # Имя вариации, которая используется для полноэкранного просмотра картинки в админке
    SHOW_VARIATION = ''

    # Имя вариации, которая показывается в админке
    ADMIN_VARIATION = ''

    # Аспекты, используемые плагином Jcrop в админке.
    # Вещественное число или кортеж вещественных чисел.
    ASPECTS = ()

    # Вариации, на которые нарезаются картинки.
    VARIATIONS = {}

    # =============================================================================

    image = GalleryImageField(_('image'),
        storage=MediaStorage(),
        upload_to=generate_filepath,
        crop_field='image_crop',
    )
    image_crop = models.CharField(_('stored_crop'),
        max_length=32,
        blank=True,
        editable=False,
    )

    class Meta:
        verbose_name = _('image item')
        verbose_name_plural = _('image items')
        abstract = True

    def __init__(self, *args, **kwargs):
        field = self._meta.get_field('image')
        if self.STORAGE_LOCATION:
            field.storage.set_directory(self.STORAGE_LOCATION)
        super().__init__(*args, **kwargs)

    def __str__(self):
        return _('Image item %(pk)s (%(path)s)') % {'pk': self.pk or 'None', 'path': self.image}

    @classmethod
    def check(cls, **kwargs):
        errors = super().check(**kwargs)
        errors.extend(cls._check_storage_location(**kwargs))
        errors.extend(cls._check_min_dimensions(**kwargs))
        errors.extend(cls._check_max_dimensions(**kwargs))
        errors.extend(cls._check_max_source_dimensions(**kwargs))
        errors.extend(cls._check_variations(**kwargs))
        errors.extend(cls._check_aspects(**kwargs))
        errors.extend(cls._check_show_variation(**kwargs))
        errors.extend(cls._check_admin_variation(**kwargs))
        return errors

    @classmethod
    def _check_storage_location(cls, **kwargs):
        if not cls.STORAGE_LOCATION:
            return [
                checks.Error(
                    'STORAGE_LOCATION is required',
                    obj=cls
                )
            ]
        elif not isinstance(cls.STORAGE_LOCATION, str):
            return [
                checks.Error(
                    'STORAGE_LOCATION must be an instance of str',
                    obj=cls
                )
            ]
        else:
            return []

    @classmethod
    def _check_min_dimensions(cls, **kwargs):
        if not cls.MIN_DIMENSIONS:
            return [
                checks.Error(
                    'MIN_DIMENSIONS is required',
                    obj=cls
                )
            ]
        elif not is_size(cls.MIN_DIMENSIONS):
            return [
                checks.Error(
                    'MIN_DIMENSIONS must be a tuple of 2 non-negative numbers',
                    obj=cls
                )
            ]
        else:
            return []

    @classmethod
    def _check_max_dimensions(cls, **kwargs):
        if not cls.MAX_DIMENSIONS:
            return [
                checks.Error(
                    'MAX_DIMENSIONS is required',
                    obj=cls
                )
            ]
        elif not is_size(cls.MAX_DIMENSIONS):
            return [
                checks.Error(
                    'MAX_DIMENSIONS must be a tuple of 2 non-negative numbers',
                    obj=cls
                )
            ]
        else:
            return []

    @classmethod
    def _check_max_source_dimensions(cls, **kwargs):
        if not cls.MAX_SOURCE_DIMENSIONS:
            return [
                checks.Error(
                    'MAX_SOURCE_DIMENSIONS is required',
                    obj=cls
                )
            ]
        elif not is_size(cls.MAX_SOURCE_DIMENSIONS):
            return [
                checks.Error(
                    'MAX_SOURCE_DIMENSIONS must be a tuple of 2 non-negative numbers',
                    obj=cls
                )
            ]
        else:
            return []

    @classmethod
    def _check_variations(cls, **kwargs):
        if not cls.VARIATIONS:
            return [
                checks.Error(
                    'VARIATIONS is required',
                    obj=cls
                )
            ]
        elif not isinstance(cls.VARIATIONS, dict):
            return [
                checks.Error(
                    'VARIATIONS must be an instance of dict',
                    obj=cls
                )
            ]

        errors = []
        errors.extend(check_variations(cls.VARIATIONS, cls))
        return errors

    @classmethod
    def _check_aspects(cls, **kwargs):
        if not cls.ASPECTS:
            return []

        errors = []
        aspects = cls.ASPECTS if isinstance(cls.ASPECTS, tuple) else (cls.ASPECTS,)
        for aspect in aspects:
            try:
                float(aspect)
            except (TypeError, ValueError):
                if not isinstance(aspect, str):
                    errors.append(
                        checks.Error(
                            'aspect can be only float or str instance',
                            obj=cls
                        )
                    )
                elif aspect not in cls.VARIATIONS:
                    errors.append(
                        checks.Error(
                            'aspect variation not found: %r' % aspect,
                            obj=cls
                        )
                    )
                elif not all(d > 0 for d in cls.VARIATIONS[aspect]['size']):
                    errors.append(
                        checks.Error(
                            'aspect should point to full-filled size: %r' % aspect,
                            obj=cls
                        )
                    )
        return errors

    @classmethod
    def _check_show_variation(cls, **kwargs):
        if cls.SHOW_VARIATION and cls.SHOW_VARIATION not in cls.VARIATIONS:
            return [
                checks.Error(
                    'SHOW_VARIATION not found in variations',
                    obj=cls
                )
            ]
        else:
            return []

    @classmethod
    def _check_admin_variation(cls, **kwargs):
        if not cls.ADMIN_VARIATION:
            return [
                checks.Error(
                    'ADMIN_VARIATION is required',
                    obj=cls
                )
            ]
        elif cls.ADMIN_VARIATION not in cls.VARIATIONS:
            return [
                checks.Error(
                    'ADMIN_VARIATION "%s" not found in variations' % cls.admin_variation,
                    obj=cls
                )
            ]
        else:
            return []

    def generate_filename(self, filename):
        if self.pk:
            return '%04d/%s' % ((self.pk // 1000), filename)
        else:
            return filename

    @classmethod
    def variations(cls):
        key = 'variations.%s.%s' % (cls.__module__, cls.__qualname__)
        variations = cls._cache.get(key)
        if variations is not None:
            return variations

        variations = format_variations(cls.VARIATIONS)
        cls._cache[key] = variations
        return variations

    @cached_property
    def admin_variation(self):
        """ Получение имени вариации для админки """
        return getattr(self.image, self.ADMIN_VARIATION, self.image)

    @property
    def show_url(self):
        if self.SHOW_VARIATION is None:
            return ''
        else:
            show_variation = getattr(self.image, self.SHOW_VARIATION, None)
            if show_variation:
                return show_variation.url

    def copy_for(self, dest_gallery, **kwargs):
        """ Создание копии текущего элемента для другой галереи """
        errors = []
        copy_fields = self.COPY_FIELDS

        new_item = dest_gallery.IMAGE_MODEL(
            gallery = dest_gallery
        )

        # image
        with self.image:
            new_item.image.save(self.image.name, self.image, save=False)

        try:
            new_item.image.field.clean(new_item.image, new_item)
        except ValidationError as e:
            new_item.image.delete()
            errors.extend(e.messages)

        for field in self._meta.concrete_fields:
            if field.name in copy_fields:
                value = getattr(self, field.name)
                setattr(new_item, field.name, value)

        return new_item, errors

    def after_copy(self, **kwargs):
        """
            Постобработка скопированного элемента.
            Параметр self - это уже новый элемент.
        """
        if self.image_crop:
            self.image.recut(croparea=self.image_crop)


class GalleryVideoLinkItem(GalleryItemBase):
    """ Элемент-видео с сервисов галереи """
    _cache = {}

    COPY_FIELDS = GalleryItemBase.COPY_FIELDS | {'video', }

    # Корневая папка (storage)
    STORAGE_LOCATION = None

    # Приблизительный размер, к которому приводятся исходники картинок
    MAX_SOURCE_DIMENSIONS = MAX_SOURCE_DIMENSIONS_DEFAULT

    # Качество исходника в случае, когда он сохраняется через PIL
    SOURCE_QUALITY = 90

    # Качество картинок вариаций по умолчанию
    DEFAULT_QUALITY = 85

    # Имя вариации, которая показывается в админке
    ADMIN_VARIATION = 'small'

    # Вариации, на которые нарезаются картинки.
    VARIATIONS = dict(
        normal=dict(
            size=(640, 360),
        ),
        medium=dict(
            size=(480, 270),
        ),
        small=dict(
            size=(320, 180),
        ),
        micro=dict(
            size=(160, 90),
        ),
    )

    # =============================================================================

    video = VideoLinkField(_('video'))
    video_preview = GalleryVideoLinkPreviewField(_('preview'),
        storage=MediaStorage(),
        upload_to=generate_filepath,
    )

    class Meta:
        verbose_name = _('video item')
        verbose_name_plural = _('video items')
        abstract = True

    def __init__(self, *args, **kwargs):
        field = self._meta.get_field('video_preview')
        if self.STORAGE_LOCATION:
            field.storage.set_directory(self.STORAGE_LOCATION)
        super().__init__(*args, **kwargs)

    def __str__(self):
        return _('Video item %(pk)s (%(path)s)') % {
            'pk': self.pk or 'None',
            'path': self.video.db_value
        }

    def save(self, *args, **kwargs):
        if self.video and self.video.info:
            preview_url = self.video.info['preview_url']
            try:
                uploaded_file = upload_file(preview_url)
            except ConnectionError:
                pass
            except URLError:
                pass
            else:
                self.video_preview.save(uploaded_file.name, uploaded_file, save=False)
                uploaded_file.close()

        super().save(*args, **kwargs)

    @classmethod
    def check(cls, **kwargs):
        errors = super().check(**kwargs)
        errors.extend(cls._check_storage_location(**kwargs))
        errors.extend(cls._check_max_source_dimensions(**kwargs))
        errors.extend(cls._check_variations(**kwargs))
        errors.extend(cls._check_admin_variation(**kwargs))
        return errors

    @classmethod
    def _check_storage_location(cls, **kwargs):
        if not cls.STORAGE_LOCATION:
            return [
                checks.Error(
                    'STORAGE_LOCATION is required',
                    obj=cls
                )
            ]
        elif not isinstance(cls.STORAGE_LOCATION, str):
            return [
                checks.Error(
                    'STORAGE_LOCATION must be an instance of str',
                    obj=cls
                )
            ]
        else:
            return []

    @classmethod
    def _check_max_source_dimensions(cls, **kwargs):
        if not cls.MAX_SOURCE_DIMENSIONS:
            return [
                checks.Error(
                    'MAX_SOURCE_DIMENSIONS is required',
                    obj=cls
                )
            ]
        elif not is_size(cls.MAX_SOURCE_DIMENSIONS):
            return [
                checks.Error(
                    'MAX_SOURCE_DIMENSIONS must be a tuple of 2 non-negative numbers',
                    obj=cls
                )
            ]
        else:
            return []

    @classmethod
    def _check_variations(cls, **kwargs):
        if not cls.VARIATIONS:
            return [
                checks.Error(
                    'VARIATIONS is required',
                    obj=cls
                )
            ]
        elif not isinstance(cls.VARIATIONS, dict):
            return [
                checks.Error(
                    'VARIATIONS must be an instance of dict',
                    obj=cls
                )
            ]

        errors = []
        errors.extend(check_variations(cls.VARIATIONS, cls))
        return errors

    @classmethod
    def _check_admin_variation(cls, **kwargs):
        if not cls.ADMIN_VARIATION:
            return [
                checks.Error(
                    'ADMIN_VARIATION is required',
                    obj=cls
                )
            ]
        elif cls.ADMIN_VARIATION not in cls.VARIATIONS:
            return [
                checks.Error(
                    'ADMIN_VARIATION "%s" not found in variations' % cls.admin_variation,
                    obj=cls
                )
            ]
        else:
            return []

    def generate_filename(self, filename):
        if self.pk:
            return 'video_%04d/%s' % ((self.pk // 1000), filename)
        else:
            return filename

    @classmethod
    def variations(cls):
        key = 'variations.%s.%s' % (cls.__module__, cls.__qualname__)
        variations = cls._cache.get(key)
        if variations is not None:
            return variations

        variations = format_variations(cls.VARIATIONS)
        cls._cache[key] = variations
        return variations

    @cached_property
    def admin_variation(self):
        """ Получение имени вариации для админки """
        return getattr(self.video_preview, self.ADMIN_VARIATION, self.video_preview)

    @property
    def show_url(self):
        return self.video.url

    def copy_for(self, dest_gallery, **kwargs):
        """ Создание копии текущего элемента для другой галереи """
        errors = []
        copy_fields = self.COPY_FIELDS

        new_item = dest_gallery.VIDEO_LINK_MODEL(
            gallery = dest_gallery
        )
        for field in self._meta.concrete_fields:
            if field.name in copy_fields:
                value = getattr(self, field.name)
                setattr(new_item, field.name, value)

        return new_item, errors


class GalleryBase(models.Model):
    """
        Базовая модель галереи.
    """
    # Модели элементов, использумые галереей
    IMAGE_MODEL = None
    VIDEO_LINK_MODEL = None

    # Размер элемента галереи в админке
    ADMIN_ITEM_SIZE = (160, 120)

    # Шаблоны поля галереи для админки
    ADMIN_TEMPLATE = 'gallery/admin/gallery.html'
    ADMIN_TEMPLATE_EMPTY = 'gallery/admin/gallery_empty.html'
    ADMIN_TEMPLATE_ITEMS = 'gallery/admin/gallery_items.html'

    # ===========================================================

    items = generic.GenericRelation(GalleryItemBase, for_concrete_model=False)

    class Meta:
        verbose_name = _('gallery')
        verbose_name_plural = _('galleries')
        abstract = True

    @classmethod
    def check(cls, **kwargs):
        errors = super().check(**kwargs)
        errors.extend(cls._check_image_model(**kwargs))
        errors.extend(cls._check_videolink_model(**kwargs))
        errors.extend(cls._check_admin_item_size(**kwargs))
        return errors

    @classmethod
    def _check_image_model(cls, **kwargs):
        if cls.IMAGE_MODEL and not issubclass(cls.IMAGE_MODEL, GalleryImageItem):
            return [
                checks.Error(
                    'IMAGE_MODEL should be a subclass of GalleryImageItem',
                    obj=cls
                )
            ]
        else:
            return []

    @classmethod
    def _check_videolink_model(cls, **kwargs):
        if cls.VIDEO_LINK_MODEL and not issubclass(cls.VIDEO_LINK_MODEL, GalleryVideoLinkItem):
            return [
                checks.Error(
                    'VIDEO_LINK_MODEL should be a subclass of GalleryVideoLinkItem',
                    obj=cls
                )
            ]
        else:
            return []

    @classmethod
    def _check_admin_item_size(cls, **kwargs):
        if not cls.ADMIN_ITEM_SIZE:
            return [
                checks.Error(
                    'ADMIN_ITEM_SIZE is required',
                    obj=cls
                )
            ]
        elif not is_size(cls.ADMIN_ITEM_SIZE):
            return [
                checks.Error(
                    'ADMIN_ITEM_SIZE should be a tuple of 2 non-negative numbers',
                    obj=cls
                )
            ]
        else:
            return []

    def __str__(self):
        return _('Gallery %(pk)s') % {'pk': self.pk}

    @cached_property
    def all_items(self):
        return self.items.all()

    @cached_property
    def image_items(self):
        return self.all_items.filter(model=self.IMAGE_MODEL)

    @cached_property
    def video_link_items(self):
        return self.all_items.filter(model=self.VIDEO_LINK_MODEL)

    def copy_items_to(self, dest_gallery, items=(), **kwargs):
        """
            Копирование картинок из одной галереи в другую.

            Параметры:
                dest_gallery - экземпляр галереи-приемника.
                items - последовательность экземпляров GalleryItemBase или ID элементов
                        галереи-источника. Если не указан - копирует все элементы.

            Можно передавать дополнительные именованые аргументы, принимаемые
            методами copy_for элементов галереи.

            Возвращает кортеж двух словарей:
                словарь ID(старый ID -> новый ID)
                словарь ошибок(ID -> текст ошибок)
        """
        success = {}
        errors = {}

        if not items:
            items = self.all_items
        elif not all(isinstance(item, GalleryItemBase) for item in items):
            items = tuple(int(item) for item in items)
            items = self.items.filter(pk__in=items)

        for item in items:
            if item.gallery != self:
                errors[item.pk] = _('Item belongs to another gallery')
                continue

            new_item, item_errors = item.copy_for(dest_gallery, **kwargs)
            if item_errors:
                errors[item.pk] = ', '.join(item_errors)
                continue

            new_item.clean()
            new_item.save()
            new_item.after_copy(**kwargs)
            success[item.pk] = new_item.pk
        return success, errors

    def recut_generator(self):
        """
            Генератор перенарезки всех картинок галереи.

            Пример:
                for error_code, msg in gallery.recut_generator():
                    print(msg)
                    if error_code:
                        break
        """
        image_items = list(self.image_items)
        for item in image_items:
            if not item.image:
                yield 1, 'Error (ID %d): Empty value' % item.pk
                continue

            if not item.image.exists():
                yield 2, 'Error (ID %d): Not found %r' % (item.pk, item.image.url)
                continue

            item.image.recut()
            yield 0, item.image.url
