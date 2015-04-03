from django.utils.image import Image
from django.conf import settings
from django.core.files.base import ContentFile
from libs.variation_field import *
from libs.checks import FieldChecksMixin
from .formfields import StdImageFormField

MAX_SIZE_DEFAULT = getattr(settings,  'STDIMAGE_MAX_SIZE_DEFAULT', 12*1024*1024)
MIN_DIMENSIONS_DEFAULT = getattr(settings,  'STDIMAGE_MIN_DIMENSIONS_DEFAULT', (0, 0))
MAX_DIMENSIONS_DEFAULT = getattr(settings,  'STDIMAGE_MAX_DIMENSIONS_DEFAULT', (6000, 6000))
MAX_SOURCE_DIMENSIONS_DEFAULT = getattr(settings,  'STDIMAGE_MAX_SOURCE_DIMENSIONS_DEFAULT', (2048, 2048))


class StdImageFieldFile(VariationImageFieldFile):

    def save(self, name, *args, **kwargs):
        setattr(self.instance, '_{}_new_file'.format(self.field.name), True)
        super().save(name, *args, **kwargs)

    def recut(self, *args, **kwargs):
        super().recut(*args, **kwargs)

        # Устанавливаем значение кропа в поле
        if self.field.crop_field:
            setattr(self.instance, self.field.crop_field, ':'.join(str(x) for x in self.cropsize))
            self.instance.save()

    def delete(self, *args, **kwargs):
        """ Удаление картинки """
        if not self:
            return

        # Сброс значения кропа в поле
        if self.field.crop_field:
            setattr(self.instance, self.field.crop_field, '')

        super().delete(*args, **kwargs)


class StdImageField(FieldChecksMixin, VariationImageField):
    attr_class = StdImageFieldFile
    
    def __init__(self, verbose_name=None, name=None, variations=None, **kwargs):
        self.admin_variation = kwargs.pop('admin_variation', None)
        self.min_dimensions = kwargs.pop('min_dimensions', MIN_DIMENSIONS_DEFAULT)
        self.max_dimensions = kwargs.pop('max_dimensions', MAX_DIMENSIONS_DEFAULT)
        self.max_source_dimensions = kwargs.pop('max_source_dimensions', MAX_SOURCE_DIMENSIONS_DEFAULT)
        self.max_size = kwargs.pop('max_size', MAX_SIZE_DEFAULT)

        self.crop_area = kwargs.pop('crop_area', False)
        self.crop_field = kwargs.pop('crop_field', None)

        # Форматируем вариации
        self._variations = variations
        self.variations = format_variations(variations)

        # Аспекты кропа. По умолчанию будет использоваться первый. Остальные можно использовать с помощью JS
        self._aspects = kwargs.pop('aspects', ())
        self.aspects = format_aspects(self._aspects, self._variations)
        
        super().__init__(verbose_name, name, **kwargs)

    def custom_check(self):
        errors = []
        if not is_size(self.min_dimensions):
            errors.append(
                self.check_error('min_dimensions should be a tuple of 2 non-negative numbers')
            )
        if not is_size(self.max_dimensions):
            errors.append(
                self.check_error('max_dimensions should be a tuple of 2 non-negative numbers')
            )
        if not is_size(self.max_source_dimensions):
            errors.append(
                self.check_error('max_source_dimensions should be a tuple of 2 non-negative numbers')
            )
        
        if not self._variations:
            errors.append(
                self.check_error('variations required')
            )
        if not isinstance(self._variations, dict):
            errors.append(
                self.check_error('variations should be a dict')
            )
        errors.extend(check_variations(self._variations, self))
        
        if self._aspects:
            aspects = self._aspects if isinstance(self._aspects, tuple) else (self._aspects, )
            for aspect in aspects:
                try:
                    float(aspect)
                except (TypeError, ValueError):
                    if not isinstance(aspect, str) or aspect not in self._variations:
                        errors.append(
                            self.check_error('invalid variation aspect: %r' % aspect)
                        )
        if not self.admin_variation:
            errors.append(
                self.check_error('admin_variation required')
            )
        return errors

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs['aspects'] = self._aspects
        kwargs['variations'] = self._variations
        if self.min_dimensions != MIN_DIMENSIONS_DEFAULT:
            kwargs['min_dimensions'] = self.min_dimensions
        if self.max_dimensions != MAX_DIMENSIONS_DEFAULT:
            kwargs['max_dimensions'] = self.max_dimensions
        if self.max_source_dimensions != MAX_SOURCE_DIMENSIONS_DEFAULT:
            kwargs['max_source_dimensions'] = self.max_source_dimensions
        if self.max_size != MAX_SIZE_DEFAULT:
            kwargs['max_size'] = self.max_size
        return name, path, args, kwargs

    def formfield(self, **kwargs):
        defaults = {
            'form_class': StdImageFormField,
            'variations': self.variations,
            'admin_variation': self.admin_variation,
            'crop_area': self.crop_area,
            'crop_field': self.crop_field,
            'min_dimensions': self.min_dimensions,
            'max_dimensions': self.max_dimensions,
            'aspects': self.aspects,
        }
        defaults.update(kwargs)
        return super().formfield(**defaults)

    def save_form_data(self, instance, data):
        final_data, delete, cropsize = data
        if delete:
            final_data = ''
            self.post_delete(instance)

        setattr(instance, '_{}_new_file'.format(self.name), final_data != getattr(instance, self.name, ''))
        setattr(instance, '_{}_cropsize'.format(self.name), cropsize)

        super().save_form_data(instance, final_data)

    def get_variations(self, instance):
        """ Возвращает настройки вариаций """
        return self.variations

    def get_min_dimensions(self, instance):
        """ Возвращает минимальные размеры картинки для загрузки """
        return self.min_dimensions
    
    def get_max_dimensions(self, instance):
        """ Возвращает максимальные размеры картинки для загрузки """
        return self.max_dimensions
    
    def get_max_size(self, instance):
        """ Возвращает максимальный вес картинки для загрузки """
        return self.max_size
    
    def build_source_name(self, instance, ext):
        """ Построение имени файла исходника """
        return '%s_%s.%s' % (self.name, instance.pk, ext.lower())

    def post_save(self, instance, **kwargs):
        """ Обработчик сигнала сохранения экземпляра модели """
        field_file = getattr(instance, self.name)
        if not field_file or not field_file.exists():
            return

        new_file_attrname = '_{}_new_file'.format(self.name)
        cropsize_attrname = '_{}_cropsize'.format(self.name)

        # Флаг, что загружен новый файл
        new_file_uploaded = getattr(instance, new_file_attrname, False)

        # Координаты обрезки
        cropsize = getattr(instance, cropsize_attrname, None)

        # Если не загрузили новый файл и не обрезали старый исходник - выходим
        if not new_file_uploaded and not cropsize:
            return
        
        # Удаляем временные атрибуты
        if hasattr(instance, new_file_attrname):
            delattr(instance, new_file_attrname)
        if hasattr(instance, cropsize_attrname):
            delattr(instance, cropsize_attrname)

        draft_size = None
        try:
            field_file.open()
            source_img = Image.open(field_file)
            source_format = source_img.format
            source_info = source_img.info

            if new_file_uploaded:
                draft_size = limited_size(source_img.size, self.max_source_dimensions)
                if draft_size is not None:
                    old_width = source_img.size[0]
                    draft = source_img.draft(None, draft_size)
                    if draft is None:
                        source_img = source_img.resize(draft_size, Image.LINEAR)
                    
                    # Учитываем изменение размера исходника на области обрезки
                    field_file.cropsize = cropsize
                    if field_file.cropsize:
                        decr_realation = old_width / source_img.size[0]
                        cropsize = tuple(round(coord / decr_realation) for coord in field_file.cropsize)

            source_img.load()
        finally:
            field_file.close()

        # Путь к исходнику
        out_name = self.build_source_name(instance, source_format)
        source_path = self.generate_filename(instance, out_name)
        source_path = self.storage.get_available_name(source_path)

        # Устанавливаем значение кропа в поле
        if cropsize and self.crop_field:
            field_file.cropsize = cropsize
            setattr(instance, self.crop_field, ':'.join(str(x) for x in field_file.cropsize))
            if not new_file_uploaded:
                instance.save()

        # Сохраняем исходник
        if new_file_uploaded:
            if draft_size is None:
                # Если картинка не менялась - копируем файл
                with self.storage.open(field_file.name) as source:
                    self.storage.save(source_path, source)
            else:
                ct = ContentFile(b'')
                
                source_info['quality'] = self.get_source_quality(instance)
                try:
                    source_img.save(ct, source_format, optimize=1, **source_info)
                except IOError:
                    source_img.save(ct, source_format, **source_info)
                
                self.storage.save(source_path, ct)

            # Удаляем загруженный исходник
            self.storage.delete(field_file.name)

            # Записываем путь к исходнику
            setattr(instance, self.attname, source_path)
            instance.save()

        # Обрабатываем вариации
        self.build_variation_images(instance, source_img, source_format, crop=cropsize)
