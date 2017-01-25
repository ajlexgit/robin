import os
import logging
from PIL import Image
from django.db import models
from django.db.models import signals
from django.core.files.images import ImageFile
from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import filesizeformat
from django.db.models.fields.files import ImageFieldFile, FieldFile, ImageFileDescriptor
from .croparea import CropArea
from .utils import (put_on_bg, limited_size, variation_crop, variation_resize,
                    variation_watermark, variation_overlay, variation_mask)

logger = logging.getLogger('variation_field')


class VariationField(ImageFile):
    """
        Класс вариации у поля экземпляра модели.
    """
    _file = None

    def __init__(self, name, storage=None, variation_size=(0, 0)):
        super().__init__(None, name)
        self.storage = storage or default_storage
        self.variation_size = variation_size

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
    def target_width(self):
        """
            Целевая ширина вариации.
            Для задания атрибута "width" у тэга "img".
        """
        return self.variation_size[0] or self.dimensions[0]

    @property
    def target_height(self):
        """
            Целевая высота вариации.
            Для задания атрибута "height" у тэга "img".
        """
        return self.variation_size[1] or self.dimensions[1]

    @property
    def path(self):
        return self.storage.path(self.name)

    @property
    def url(self):
        return self.storage.url(self.name)

    @property
    def url_nocache(self):
        if self.storage.exists(self.name):
            return self.storage.url(self.name) + '?_=%d' % self.storage.modified_time(self.name).timestamp()
        else:
            return self.storage.url(self.name)

    @property
    def srcset(self):
        width = self.variation_size[0] or self.dimensions[0]
        return '{url} {width}w'.format(url=self.url, width=width)

    @property
    def srcset_nocache(self):
        width = self.dimensions[0]
        return '{url} {width}w'.format(url=self.url_nocache, width=width)

    @property
    def space(self):
        return '%0.2f%%' % (100 * self.height / self.width)

    @property
    def target_space(self):
        return '%0.2f%%' % (100 * self.target_height / self.target_width)

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
    _croparea = ''
    _variations = None

    def __getattr__(self, item):
        if item in self.variations:
            self.create_variations()
            if hasattr(self, item):
                return getattr(self, item)

        raise AttributeError(
            "'%s' object has no attribute '%s'" % (self.__class__.__name__, item)
        )

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
    def srcset(self):
        width = self.dimensions[0]
        return '{url} {width}w'.format(url=self.url, width=width)

    @property
    def srcset_nocache(self):
        width = self.dimensions[0]
        return '{url} {width}w'.format(url=self.url_nocache, width=width)

    @property
    def space(self):
        return '%0.2f%%' % (100 * self.height / self.width)

    @property
    def croparea(self):
        return self._croparea

    @croparea.setter
    def croparea(self, value):
        """ Форматирование области обрезки картинки """
        if value is None:
            return

        if not value:
            self._croparea = ''
        elif isinstance(value, (list, tuple)):
            self._croparea = CropArea(*value)
        elif isinstance(value, CropArea):
            self._croparea = value
        else:
            self._croparea = CropArea(value)

    @property
    def variations(self):
        if self._variations is None:
            self._variations = self.field.get_variations(self.instance)
        return self._variations

    @property
    def variation_files(self):
        """
            Возвращает кортеж путей к вариациям файла.
            Существование файлов не гарантировано.
            !!! Пути не учитывают storage !!!
        """
        files_list = []
        for name, variation in self.variations.items():
            path = self.field.build_variation_name(variation, self.name)
            files_list.append(path)
        return tuple(files_list)

    def set_crop_field(self, instance, croparea=None):
        self.croparea = croparea
        if self.field.crop_field and hasattr(instance, self.field.crop_field):
            setattr(instance, self.field.crop_field, self.croparea)

    def create_variations(self):
        """
            Создает атрибуты вариаций
        """
        if not self or not self.exists():
            return

        for name, variation in self.variations.items():
            variation_filename = self.field.build_variation_name(variation, self.name)
            variation_field = VariationField(
                variation_filename,
                storage=self.storage,
                variation_size=variation['size']
            )
            setattr(self, name, variation_field)

    def recut(self, *args, croparea=''):
        """
            Перенарезка вариаций.

            Пример:
                company.logo.recut('on_list', 'on_news')
                company.logo.recut('on_list', croparea=[0, 12, 310, 177])
        """
        # Форматирование параметров обрезки
        self.croparea = croparea

        # Обрабатываем вариации
        self.create_variations()
        for name, variation in self.variations.items():
            if args and name not in args:
                continue

            self.field.resize_image(
                self.instance,
                self.path,
                variation,
                croparea=self.croparea
            )

        if self.field.crop_field:
            self.set_crop_field(self.instance, croparea)
            self.field.update_instance(self.instance, **{
                self.field.crop_field: self.croparea
            })

    def rotate(self, angle=90):
        """
            Поворот вариаций и исходника.

            Потеряется кроп из админки, т.к. выбранная область не сохраняется.
            Углы поворота обратны углам PIL:
                положительные - по часовой стрелке
                отрицательные - против часовой стрелке

            Пример:
                company.logo.rotate(90)
        """
        try:
            self.open()
            source_image = Image.open(self)
            source_format = source_image.format

            info = dict(source_image.info)

            source_image = source_image.rotate(-angle, expand=True)
            source_image.format = source_format
            with self.storage.open(self.name, 'wb') as destination:
                try:
                    source_image.save(destination, source_format, optimize=1, **info)
                except IOError:
                    source_image.save(destination, source_format, **info)
        finally:
            self.close()

        # Сброс закэшированных размеров
        self.clear_dimensions()

        # Обрабатываем вариации
        self.create_variations()
        for name, variation in self.variations.items():
            self.field.resize_image(
                self.instance,
                self.path,
                variation,
            )

    def save(self, name, content, save=True):
        newfile_attrname = '_{}_new_file'.format(self.field.name)
        setattr(self.instance, newfile_attrname, True)
        if self.field.crop_field:
            self.set_crop_field(self.instance, '')
        super().save(name, content, save)
    save.alters_data = True

    def delete(self, save=True):
        """ Удаление картинки """
        self.create_variations()
        for name in self.variations:
            variation_field = getattr(self, name, None)
            if variation_field:
                variation_field.delete()
        if self.field.crop_field:
            self.set_crop_field(self.instance, '')
        super().delete(save)
    delete.alters_data = True


class VariationImageFileDescriptor(ImageFileDescriptor):
    def __get__(self, instance=None, owner=None):
        if instance is None:
            return owner._meta.get_field(self.field.name)

        value = super().__get__(instance, owner)

        # Добавляем значение области обрезки
        if self.field.crop_field:
            croparea = getattr(instance, self.field.crop_field)
            try:
                value.croparea = CropArea(croparea)
            except ValueError:
                pass

        return value

    def __set__(self, instance, value):
        if isinstance(value, VariationImageFieldFile):
            if self.field.crop_field:
                value.set_crop_field(instance, value.croparea)

        super().__set__(instance, value)


class VariationImageField(models.ImageField):
    attr_class = VariationImageFieldFile
    descriptor_class = VariationImageFileDescriptor

    default_error_messages = dict(
        models.ImageField.default_error_messages,
        not_image=_("Image invalid or corrupted"),
        not_enough_width=_('Image should not be less than %(limit)spx in width'),
        not_enough_height=_('Image should not be less than %(limit)spx in height'),
        too_much_width=_('Image should not be more than %(limit)spx in width'),
        too_much_height=_('Image should not be more than %(limit)spx in height'),
        too_big=_('Image must be no larger than %(limit)s'),
    )

    def __init__(self, *args, **kwargs):
        self.crop_field = kwargs.pop('crop_field', None)
        super().__init__(*args, **kwargs)

    def get_prep_value(self, value):
        if isinstance(value, FieldFile) and not value.exists():
            return ''

        return super().get_prep_value(value)

    def contribute_to_class(self, cls, name, **kwargs):
        super().contribute_to_class(cls, name, **kwargs)
        signals.post_save.connect(self._post_save, sender=cls)
        signals.post_delete.connect(self._post_delete, sender=cls)

    def save_form_data(self, instance, data):
        croparea = None
        if isinstance(data, (list, tuple)):
            data, croparea = data

        # Important: None means "no change", other false value means "clear"
        # This subtle distinction (rather than a more explicit marker) is
        # needed because we need to consume values that are also sane for a
        # regular (non Model-) Form to find in its cleaned_data dictionary.
        if data is not None:
            # This value will be converted to unicode and stored in the
            # database, so leaving False as-is is not acceptable.
            if not data:
                data = ''
                self._post_delete(instance)

            setattr(instance, self.name, data)

            if data and croparea is not None:
                setattr(instance, '_{}_croparea'.format(self.name), croparea)

    def validate_type(self, value, model_instance):
        """ Валидация типа файла """
        try:
            Image.open(value).verify()
        except Exception:
            raise ValidationError(
                self.error_messages['not_image'],
                code='not_image',
            )

    def validate_dimensions(self, value, model_instance):
        """ Валидация размеров картинки """
        img_width, img_height = value.dimensions
        croparea = value.croparea
        if croparea:
            img_width = min(croparea.width, img_width)
            img_height = min(croparea.height, img_height)

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

    def validate_size(self, value, model_instance):
        """ Валидация веса картинки """
        max_size = self.get_max_size(model_instance)
        if max_size and value.size > max_size:
            raise ValidationError(
                self.error_messages['too_big'] % {
                    'current': filesizeformat(value.size),
                    'limit': filesizeformat(max_size),
                },
                code='too_big',
            )

    def validate(self, value, model_instance):
        if value:
            self.validate_type(value, model_instance)
            self.validate_dimensions(value, model_instance)
            self.validate_size(value, model_instance)

        super().validate(value, model_instance)

    def get_variations(self, instance):
        """ Возвращает настройки вариаций """
        raise NotImplementedError()

    def get_source_quality(self, instance):
        """ Возвращает качество исходника, если он сохраняется через PIL """
        raise NotImplementedError()

    def get_variation_quality(self, instance, variation):
        """ Возвращает качество картинок вариаций по умолчанию """
        raise NotImplementedError()

    def get_max_source_dimensions(self, instance):
        """ Возвращает максимальные размеры исходника картинки """
        raise NotImplementedError()

    def get_min_dimensions(self, instance):
        """ Возвращает минимальные размеры картинки для загрузки """
        return 0, 0

    def get_max_dimensions(self, instance):
        """ Возвращает максимальные размеры картинки для загрузки """
        return 6000, 6000

    def get_max_size(self, instance):
        """ Возвращает максимальный вес картинки для загрузки """
        return 20 * 1024 * 1024

    def build_source_name(self, instance, ext):
        raise NotImplementedError()

    def save_source_file(self, instance, source_image, draft_size=None, **kwargs):
        """ Сохранение исходника """
        field_file = self.value_from_object(instance)

        if source_image.format is None:
            print('Warning: Image format is None (_save_source_file)')

        out_name = self.build_source_name(instance, source_image.format)
        source_path = self.generate_filename(instance, out_name)
        source_path = self.storage.get_available_name(source_path)

        if draft_size is None:
            # Если картинка не менялась - копируем файл
            with self.storage.open(field_file.name) as source:
                self.storage.save(source_path, source)
        else:
            params = source_image.info or {}
            params['quality'] = self.get_source_quality(instance)
            params.update(**kwargs)

            with self.storage.open(source_path, 'wb') as destination:
                try:
                    source_image.save(destination, source_image.format, optimize=1, **params)
                except IOError:
                    source_image.save(destination, source_image.format, **params)
                finally:
                    source_image.close()

        # Записываем путь к исходнику
        setattr(instance, self.attname, source_path)

        return source_path

    @staticmethod
    def update_instance(instance, **kwargs):
        if not kwargs:
            return
        if not instance.pk:
            raise ValueError('saving image to not saved instance')
        queryset = instance._meta.model.objects.filter(pk=instance.pk)
        queryset.update(**kwargs)

    @staticmethod
    def build_variation_name(variation, source_filename):
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

    def resize_image(self, instance, filepath, variation, croparea=None):
        """ Обработка и сохранение одной вариации """
        if not filepath or not os.path.exists(filepath):
            return

        field_file = self.value_from_object(instance)

        with open(filepath, 'rb') as fp:
            variation_image = Image.open(fp)

            # Обрезаем по рамке
            if not variation['use_source'] and croparea is not None:
                variation_image = variation_crop(variation_image, croparea)

            # Целевой формат
            target_format = variation['format'] or variation_image.format
            target_format = target_format.upper()

            # Параметры сохранения
            save_params = dict(
                format=target_format,
                quality=self.get_variation_quality(instance, variation),
            )

            # Изображение с режимом "P" нельзя сохранять в JPEG,
            # а в GIF - фон становится черным
            if variation_image.mode == 'P' and target_format in ('JPEG', 'GIF'):
                variation_image = variation_image.convert('RGBA')

            # При сохранении в GIF проблематично указать прозрачность. Кроме того,
            # Уменьшенный в размере прозрачный GIF ужасен по качеству. Пока накладываем на фон
            if target_format == 'GIF':
                masked = variation_image.mode == 'RGBA'
                variation_image = put_on_bg(variation_image, variation_image.size,
                    color=variation['background'][:3],
                    offset=variation['offset'],
                    masked=masked)

            # Основная обработка картинок
            variation_image = self._process_variation(variation_image, variation, target_format)

            # Сохранение
            variation_filename = self.build_variation_name(variation, field_file.name)
            with self.storage.open(variation_filename, 'wb') as destination:
                try:
                    variation_image.save(destination, optimize=1, **save_params)
                except IOError:
                    variation_image.save(destination, **save_params)

            del variation_image

        # Очищаем закэшированные размеры картинки, т.к. они могли измениться
        variation_field = getattr(field_file, variation['name'])
        variation_field.clear_dimensions()

    def build_variation_images(self, instance, croparea=None):
        """
            Обрезает картинку source_image по заданным координатам
            и создает из результата файлы вариаций.
        """
        field_file = self.value_from_object(instance)
        if not field_file or not field_file.exists():
            return

        field_file.create_variations()
        for variation in field_file.variations.values():
            self.resize_image(
                instance,
                field_file.path,
                variation,
                croparea=croparea
            )

    def _post_save(self, instance, **kwargs):
        """ Обертка над реальным обработчиком """
        # Флаг, что загружен новый файл
        new_file_attrname = '_{}_new_file'.format(self.name)
        new_file_uploaded = getattr(instance, new_file_attrname, False)
        if hasattr(instance, new_file_attrname):
            delattr(instance, new_file_attrname)

        # Координаты обрезки
        croparea_attrname = '_{}_croparea'.format(self.name)
        croparea = getattr(instance, croparea_attrname, None)
        if hasattr(instance, croparea_attrname):
            delattr(instance, croparea_attrname)

        self.post_save(instance, is_uploaded=new_file_uploaded, croparea=croparea, **kwargs)

    def post_save(self, instance, is_uploaded=None, croparea=None, **kwargs):
        """ Обработчик сигнала сохранения экземпляра модели """
        # Если не загрузили новый файл и не обрезали старый исходник - выходим
        if not is_uploaded and not croparea:
            return

        field_file = self.value_from_object(instance)
        if not field_file or not field_file.exists():
            return

        field_file.croparea = croparea

        update_fields = {}

        try:
            field_file.open()
            source_image = Image.open(field_file)
            source_format = source_image.format

            if is_uploaded:
                draft_size = limited_size(
                    source_image.size,
                    self.get_max_source_dimensions(instance)
                )
                if draft_size is not None:
                    old_width = source_image.size[0]
                    draft = source_image.draft(None, draft_size)
                    if draft is None:
                        source_image = source_image.resize(draft_size, Image.HAMMING)
                        source_image.format = source_format

                    # Учитываем изменение размера исходника на области обрезки
                    if field_file.croparea:
                        decr_relation = old_width / source_image.size[0]
                        croparea = tuple(
                            round(coord / decr_relation)
                            for coord in field_file.croparea
                        )
                        field_file.croparea = croparea

                # Сохраняем исходник
                source_path = self.save_source_file(instance, source_image, draft_size=draft_size)
                update_fields[self.attname] = source_path
        finally:
            field_file.close()

            # Удаляем загруженный исходник
            if is_uploaded:
                self.storage.delete(field_file.name)

        # Сохраняем область обрезки в поле, если оно указано
        if croparea and self.crop_field:
            update_fields[self.crop_field] = croparea

        self.update_instance(instance, **update_fields)

        # Обрабатываем вариации
        self.build_variation_images(instance, croparea=field_file.croparea)

    def _post_delete(self, instance=None, **kwargs):
        """ Обработчик сигнала удаления экземпляра модели """
        field_file = self.value_from_object(instance)
        field_file.delete(save=False)

    def recut_all(self, *args):
        """ Перенарезка всех картинок """
        if self.crop_field:
            get_crop = lambda i: getattr(i, self.crop_field)
        else:
            get_crop = lambda i: None

        for instance in self.model.objects.all():
            file_field = getattr(instance, self.name)
            if file_field:
                file_field.recut(*args, croparea=get_crop(instance))
