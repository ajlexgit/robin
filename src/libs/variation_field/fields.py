import os
from django.db.models import signals
from django.utils.image import Image
from django.core.files.images import ImageFile
from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import filesizeformat
from django.db.models.fields.files import ImageField, ImageFieldFile
from .utils import (put_on_bg, variation_crop, variation_resize, variation_watermark,
                    variation_overlay, variation_mask)

DEFAULT_SOURCE_QUALITY = 95
DEFAUL_VARIATION_QUALITY = 90


class VariationField(ImageFile):
    _file = None

    """
        Класс вариации у поля экземпляра модели.
    """
    def __init__(self, name, storage=None):
        super().__init__(None, name)
        self.storage = storage or default_storage

    @property
    def file(self):
        if not hasattr(self, '_file') or self._file is None:
            self._file = self.storage.open(self.name, 'rb')
        return self._file

    @file.setter
    def file(self, file):
        self._file = file

    @file.deleter
    def file(self):
        del self._file

    def exists(self):
        return self.storage.exists(self.name)

    def open(self, mode='rb'):
        self.file.open(mode)

    def close(self):
        file = getattr(self, '_file', None)
        if file is not None:
            file.close()

    def delete(self):
        if not self:
            return
        # Only close the file if it's already open, which we know by the
        # presence of self._file
        if hasattr(self, '_file'):
            self.close()
            del self.file

        self.storage.delete(self.name)
        self.name = None

    @property
    def dimensions(self):
        if self and (self.exists() or not self.closed):
            return self._get_image_dimensions()
        else:
            return -1, -1

    def clear_dimensions(self):
        if hasattr(self, '_dimensions_cache'):
            del self._dimensions_cache

    @property
    def path(self):
        return self.storage.path(self.name)

    @property
    def url(self):
        return self.storage.url(self.name)

    @property
    def url_nocache(self):
        return self.storage.url(self.name) + '?_=%d' % self.storage.modified_time(self.name).timestamp()

    @property
    def size(self):
        return self.storage.size(self.name)

    @property
    def accessed_time(self):
        return self.storage.accessed_time(self.name)

    @property
    def created_time(self):
        return self.storage.created_time(self.name)

    @property
    def modified_time(self):
        return self.storage.modified_time(self.name)


class VariationImageFieldFile(ImageFieldFile):
    _cropsize = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.variations = {}

    @property
    def dimensions(self):
        """ Реальные размеры изображения """
        if self and (self.exists() or not self.closed):
            return self._get_image_dimensions()
        else:
            return -1, -1

    def clear_dimensions(self):
        if hasattr(self, '_dimensions_cache'):
            del self._dimensions_cache

    def exists(self):
        return self.storage.exists(self.name)

    @property
    def url_nocache(self):
        try:
            mt = self.storage.modified_time(self.name).timestamp()
        except FileNotFoundError:
            mt = 0
        return self.storage.url(self.name) + '?_=%d' % mt

    @property
    def cropsize(self):
        return self._cropsize

    @cropsize.setter
    def cropsize(self, value):
        """ Форматирование области обрезки картинки """
        if isinstance(value, str):
            value = value.split(':')

        try:
            cropsize = tuple(int(coord) for coord in value)
        except (ValueError, TypeError):
            self._cropsize = ()
        else:
            if len(cropsize) == 4:
                self._cropsize = cropsize
            else:
                self._cropsize = ()

    def recut(self, *args, crop=None):
        """
            Перенарезка вариаций.

            Потеряется кроп из админки, т.к. выбранная область не сохраняется.
            Можно передать параметры обрезки вручну в параметре crop, в формате
            [left, top, width, height].

            Пример:
                company.logo.recut('on_list', 'on_news')
                company.logo.recut('on_list', crop=[0, 12, 310, 177])
        """
        # Форматирование параметров обрезки
        self.cropsize = crop

        with self as field_file:
            field_file.open()
            source_img = Image.open(field_file)
            source_format = source_img.format
            source_img.load()

        # Обрезаем по рамке
        temp_img = variation_crop(source_img, self.cropsize)

        # Обрабатываем вариации
        self.field._create_variation_fields(self.instance)
        for name, variation in self.variations.items():
            if args and name not in args:
                continue

            target_format = variation['format'] or source_format
            if variation['use_source']:
                self.field._resize_image(self.instance, variation, target_format, source_img)
            else:
                self.field._resize_image(self.instance, variation, target_format, temp_img)

        # Освобожение ресурсов
        source_img.close()

    def rotate(self, angle=90, quality=None):
        """
            Поворот вариаций и исходника.

            Потеряется кроп из админки, т.к. выбранная область не сохраняется.
            Углы поворота обратны углам PIL:
                положительные - по часовой стрелке
                отрицательные - против часовой стрелке

            Пример:
                company.logo.rotate(90)
        """
        quality = quality or self.field.get_source_quality(self.instance)

        with self as field_file:
            field_file.open()
            source_img = Image.open(field_file)
            source_format = source_img.format
            source_img.load()

        info = dict(source_img.info,
            quality=quality,
        )

        source_img = source_img.rotate(-angle)
        with self.storage.open(self.name, 'wb') as destination:
            try:
                source_img.save(destination, source_format, optimize=1, **info)
            except IOError:
                source_img.save(destination, source_format, **info)

        # Сброс закэшированных размеров
        self.clear_dimensions()

        # Обрабатываем вариации
        self.field._create_variation_fields(self.instance)
        for name, variation in self.variations.items():
            target_format = variation['format'] or source_format
            self.field._resize_image(self.instance, variation, target_format, source_img)

        # Освобожение ресурсов
        source_img.close()

    def delete(self, save=True):
        """ Удаление картинки """
        self.field._create_variation_fields(self.instance)
        for name in self.variations:
            variation_field = getattr(self, name, None)
            if variation_field:
                variation_field.delete()

        super().delete(save)


class VariationImageField(ImageField):

    default_error_messages = dict(
        ImageField.default_error_messages,
        not_image=_("Upload a valid image. The file you uploaded was either not an image or a corrupted image."),
        not_enough_width=_('Image width should not be less than %(limit)s pixels'),
        not_enough_height=_('Image height should not be less than %(limit)s pixels'),
        too_much_width=_('Image width should not be greater than %(limit)s pixels'),
        too_much_height=_('Image height should not be greater than %(limit)s pixels'),
        too_big=_('Image width should not be greater than %(limit)s'),
    )

    def _create_variation_fields(self, instance):
        """ Создание полей вариаций, если их нет """
        field_file = getattr(instance, self.name)
        if not field_file.variations:
            self._set_field_variations(instance)

    def _set_field_variations(self, instance, **kwargs):
        """
            Создает в экземпляре класса VariationImageFieldFile поля вариаций
        """
        field_file = getattr(instance, self.name)
        field_file.variations = self.get_variations(instance)
        if not field_file or not field_file.exists():
            return

        for name, variation in field_file.variations.items():
            variation_filename = self._build_variation_name(variation, field_file.name)
            variation_field = VariationField(variation_filename, storage=self.storage)
            setattr(field_file, name, variation_field)

    @staticmethod
    def _build_variation_name(variation, source_filename):
        """ Возвращает имя файла вариации """
        basename, ext = os.path.splitext(source_filename)
        image_format = variation['format']
        if image_format:
            ext = '.%s' % image_format.lower()
        return ''.join((basename, '.%s' % variation['name'], ext))

    @staticmethod
    def _process_variation(image, variation, target_format):
        """ Обработка картинки для сохранения в качестве вариации """
        image = variation_resize(image, variation, target_format)
        image = variation_watermark(image, variation)
        image = variation_overlay(image, variation)
        image = variation_mask(image, variation)
        return image

    def _resize_image(self, instance, variation, target_format, source_image):
        """ Обработка и сохранение одной вариации """
        field_file = getattr(instance, self.name)
        if not field_file or not field_file.exists():
            return

        variation_image = source_image.copy()

        # Целевой формат
        target_format = target_format.upper()

        # Параметры сохранения
        save_params = dict(
            format = target_format,
            quality = variation['quality'] or self.get_default_quality(instance),
        )

        # Изображение с режимом "P" нельзя сохранять в JPEG,
        # а в GIF - фон становится черным
        if variation_image.mode == 'P' and target_format in ('JPEG', 'GIF'):
            variation_image = variation_image.convert('RGBA')

        # При сохранении в GIF проблематично указать прозрачность. Кроме того,
        # Уменьшенный в размере прозрачный GIF ужасен по качеству. Пока накладываем на фон
        if target_format == 'GIF':
            masked = variation_image.mode == 'RGBA'
            variation_image = put_on_bg(variation_image, variation_image.size, variation['background'][:3],
                                        variation['position'], masked)

        # Основная обработка картинок
        variation_image = self._process_variation(variation_image, variation, target_format)

        # Сохранение
        variation_filename = self._build_variation_name(variation, field_file.name)
        with self.storage.open(variation_filename, 'wb') as destination:
            try:
                variation_image.save(destination, optimize=1, **save_params)
            except IOError:
                variation_image.save(destination, **save_params)

        # Очищаем закэшированные размеры картинки, т.к. они могли измениться
        variation_field = getattr(field_file, variation['name'])
        variation_field.clear_dimensions()

    def get_prep_value(self, value):
        if value and value.exists():
            return super().get_prep_value(value)
        else:
            return ''

    def contribute_to_class(self, cls, name):
        super().contribute_to_class(cls, name)
        signals.post_save.connect(self.post_save, sender=cls)
        signals.post_init.connect(self._set_field_variations, sender=cls)
        signals.post_delete.connect(self.post_delete, sender=cls)

    def validate(self, value, model_instance):
        if value:
            try:
                Image.open(value).verify()
            except Exception:
                raise ValidationError(
                    self.error_messages['not_image'],
                    code='not_image',
                )

            img_width, img_height = value.dimensions
            if value.cropsize:
                img_width = min(value.cropsize[2], img_width)
                img_height = min(value.cropsize[3], img_height)

            min_width, min_height = self.get_min_dimensions(model_instance)
            if min_width and img_width < min_width:
                raise ValidationError(
                    self.error_messages['not_enough_width'] % {
                        'current': img_width,
                        'limit': min_width,
                    },
                    code='not_enough_width',
                )
            if min_height and img_height < min_height:
                raise ValidationError(
                    self.error_messages['not_enough_height'] % {
                        'current': img_height,
                        'limit': min_height,
                    },
                    code='not_enough_height',
                )

            max_width, max_height = self.get_max_dimensions(model_instance)
            if max_width and img_width > max_width:
                raise ValidationError(
                    self.error_messages['too_much_width'] % {
                        'current': img_width,
                        'limit': max_width,
                    },
                    code='too_much_width',
                )
            if max_height and img_height > max_height:
                raise ValidationError(
                    self.error_messages['too_much_height'] % {
                        'current': img_height,
                        'limit': max_height,
                    },
                    code='too_much_height',
                )

            max_size = self.get_max_size(model_instance)
            if max_size and value.size > max_size:
                raise ValidationError(
                    self.error_messages['too_big'] % {
                        'current': filesizeformat(value.size),
                        'limit': filesizeformat(max_size),
                    },
                    code='too_big',
                )

        super().validate(value, model_instance)

    def get_variations(self, instance):
        """ Возвращает настройки вариаций """
        raise NotImplementedError()

    def get_source_quality(self, instance):
        """ Возвращает качество исходника, если он сохраняется через PIL """
        return DEFAULT_SOURCE_QUALITY

    def get_default_quality(self, instance):
        """ Возвращает качество картинок вариаций по умолчанию """
        return DEFAUL_VARIATION_QUALITY

    def get_min_dimensions(self, instance):
        """ Возвращает минимальные размеры картинки для загрузки """
        raise NotImplementedError()

    def get_max_dimensions(self, instance):
        """ Возвращает максимальные размеры картинки для загрузки """
        raise NotImplementedError()

    def get_max_size(self, instance):
        """ Возвращает максимальный вес картинки для загрузки """
        raise NotImplementedError()

    def build_variation_images(self, instance, source_image, source_format, crop=None):
        """
            Обрезает картинку source_image по заданным координатам
            и создает из результата файлы вариаций.
        """
        field_file = getattr(instance, self.name)

        if crop:
            field_file.cropsize = crop
            current_image = variation_crop(source_image, field_file.cropsize)
        else:
            current_image = source_image

        self._create_variation_fields(instance)
        for name, variation in field_file.variations.items():
            target_format = variation['format'] or source_format
            if variation.get('use_source'):
                self._resize_image(instance, variation, target_format, source_image)
            else:
                self._resize_image(instance, variation, target_format, current_image)

    def post_save(self, instance, **kwargs):
        """ Обработчик сигнала сохранения экземпляра модели """
        raise NotImplementedError()

    def post_delete(self, instance=None, **kwargs):
        """ Обработчик сигнала удаления экземпляра модели """
        field_file = getattr(instance, self.name)
        field_file.delete(save=False)
