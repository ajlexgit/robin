import os
from django.db import models
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
from libs.checks import ModelChecksMixin
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


class GalleryItemBase(ModelChecksMixin, models.Model):
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

    order = models.PositiveIntegerField(_('order'), default=0)
    created = models.DateTimeField(_('created on'))
    changed = models.DateTimeField(_('changed on'), auto_now=True)

    objects = GalleryItemQuerySet.as_manager()

    class Meta:
        verbose_name = _('gallery item')
        verbose_name_plural = _('gallery items')
        ordering = ('object_id', 'order', 'created', )
        index_together = (('content_type', 'object_id'), )

    def save(self, *args, **kwargs):
        is_add = not self.pk
        if is_add:
            self.self_type = ContentType.objects.get_for_model(type(self), for_concrete_model=False)
            self.created = now()

            order = self.gallery.items.aggregate(max=models.Max('order')).get('max', 0)
            self.order = 0 if order is None else order + 1

        super().save(*args, **kwargs)

    @classmethod
    def custom_check(cls):
        """ Проверка модели """
        errors = []
        if not isinstance(cls.COPY_FIELDS, set):
            errors.append(
                cls.check_error('COPY_FIELDS should be an instance of set')
            )
        return errors

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
        upload_to=generate_filepath
    )
    crop = models.CharField(_('image crop coordinates'), max_length=32, blank=False)

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
    def custom_check(cls):
        """ Проверка модели """
        errors = super().custom_check()
        if not cls.STORAGE_LOCATION:
            errors.append(
                cls.check_error('STORAGE_LOCATION required')
            )
        if not is_size(cls.MIN_DIMENSIONS):
            errors.append(
                cls.check_error('MIN_DIMENSIONS should be a tuple of 2 non-negative numbers')
            )
        if not is_size(cls.MAX_DIMENSIONS):
            errors.append(
                cls.check_error('MAX_DIMENSIONS should be a tuple of 2 non-negative numbers')
            )
        if not is_size(cls.MAX_SOURCE_DIMENSIONS):
            errors.append(
                cls.check_error('MAX_SOURCE_DIMENSIONS should be a tuple of 2 non-negative numbers')
            )

        if not cls.VARIATIONS:
            errors.append(
                cls.check_error('VARIATIONS required')
            )
        if not isinstance(cls.VARIATIONS, dict):
            errors.append(
                cls.check_error('VARIATIONS should be a dict')
            )
        errors.extend(check_variations(cls.VARIATIONS, cls))

        if cls.ASPECTS:
            aspects = cls.ASPECTS if isinstance(cls.ASPECTS, tuple) else (cls.ASPECTS, )
            for aspect in aspects:
                try:
                    float(aspect)
                except (TypeError, ValueError):
                    if not isinstance(aspect, str) or aspect not in cls.VARIATIONS:
                        errors.append(
                            cls.check_error('invalid variation aspect: %r' % aspect)
                        )
                    elif not all(d > 0 for d in cls.VARIATIONS[aspect]['size']):
                        errors.append(
                            cls.check_error('aspect should point to full-filled size: %r' % aspect)
                        )

        if cls.SHOW_VARIATION and cls.SHOW_VARIATION not in cls.VARIATIONS:
            errors.append(
                cls.check_error('SHOW_VARIATION %r not found in VARIATIONS' % cls.SHOW_VARIATION)
            )
        if not cls.ADMIN_VARIATION:
            errors.append(
                cls.check_error('ADMIN_VARIATION required')
            )
        if cls.ADMIN_VARIATION not in cls.VARIATIONS:
            errors.append(
                cls.check_error('ADMIN_VARIATION %r not found in VARIATIONS' % cls.ADMIN_VARIATION)
            )
        return errors

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
        copy_fields = self.COPY_FIELDS.copy()

        # Если указан параметр crop_images - копируем кроп картинки
        crop_images = kwargs.get('crop_images', False)
        if crop_images:
            copy_fields.add('crop')

        new_item = dest_gallery.IMAGE_MODEL(
            gallery = dest_gallery
        )
        for field in self._meta.concrete_fields:
            if field.name in copy_fields:
                value = getattr(self, field.name)
                setattr(new_item, field.name, value)

        # image
        with self.image:
            new_item.image.save(self.image.name, self.image, save=False)

        try:
            new_item.image.field.clean(new_item.image, new_item)
        except ValidationError as e:
            new_item.image.delete()
            errors.extend(e.messages)

        return new_item, errors

    def after_copy(self, **kwargs):
        """
            Постобработка скопированного элемента.
            Параметр self - это уже новый элемент.
        """
        if self.crop:
            self.image.recut(crop=self.crop)


class GalleryVideoLinkItem(GalleryItemBase):
    """ Элемент-видео с сервисов галереи """
    _cache = {}

    COPY_FIELDS = GalleryItemBase.COPY_FIELDS | {'video', }

    # Корневая папка (storage)
    STORAGE_LOCATION = None

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
    def custom_check(cls):
        """ Проверка модели """
        errors = super().custom_check()
        if not cls.STORAGE_LOCATION:
            errors.append(
                cls.check_error('STORAGE_LOCATION required')
            )
        if not cls.VARIATIONS:
            errors.append(
                cls.check_error('VARIATIONS required')
            )
        if not isinstance(cls.VARIATIONS, dict):
            errors.append(
                cls.check_error('VARIATIONS should be a dict')
            )
        if not cls.ADMIN_VARIATION:
            errors.append(
                cls.check_error('ADMIN_VARIATION required')
            )
        if cls.ADMIN_VARIATION not in cls.VARIATIONS:
            errors.append(
                cls.check_error('ADMIN_VARIATION %r not found in VARIATIONS' % cls.ADMIN_VARIATION)
            )
        errors.extend(check_variations(cls.VARIATIONS, cls))
        return errors

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


class GalleryBase(ModelChecksMixin, models.Model):
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
    def custom_check(cls):
        """ Проверка модели """
        errors = []
        if cls.IMAGE_MODEL and not issubclass(cls.IMAGE_MODEL, GalleryImageItem):
            errors.append(
                cls.check_error('IMAGE_MODEL should be a subclass of GalleryImageItem')
            )
        if cls.VIDEO_LINK_MODEL and not issubclass(cls.VIDEO_LINK_MODEL, GalleryVideoLinkItem):
            errors.append(
                cls.check_error('VIDEO_LINK_MODEL should be a subclass of GalleryVideoLinkItem')
            )
        if not is_size(cls.ADMIN_ITEM_SIZE):
            errors.append(
                cls.check_error('ADMIN_ITEM_SIZE should be a tuple of 2 non-negative numbers')
            )
        return errors

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

            Также можно передавать дополнительные именованые аргументы, принимаемые
            методами copy_for элементов галереи. Например:
                crop_images - если истинен, при копировании картинок будут скопированы их области
                              обрезки и проведена перенарезка.

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

            item.image.recut(crop=item.crop)
            yield 0, item.image.url
