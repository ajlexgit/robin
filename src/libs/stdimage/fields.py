from django.core import checks
from django.conf import settings
from django.utils.image import Image
from libs.variation_field import *
from .formfields import StdImageFormField

DEFAULT_SOURCE_QUALITY = 95
DEFAULT_VARIATION_QUALITY = 90
MAX_SIZE_DEFAULT = getattr(settings,  'STDIMAGE_MAX_SIZE_DEFAULT', 12*1024*1024)
MIN_DIMENSIONS_DEFAULT = getattr(settings,  'STDIMAGE_MIN_DIMENSIONS_DEFAULT', (0, 0))
MAX_DIMENSIONS_DEFAULT = getattr(settings,  'STDIMAGE_MAX_DIMENSIONS_DEFAULT', (6000, 6000))
MAX_SOURCE_DIMENSIONS_DEFAULT = getattr(settings,  'STDIMAGE_MAX_SOURCE_DIMENSIONS_DEFAULT', (2048, 2048))


class StdImageField(VariationImageField):

    def __init__(self, verbose_name=None, name=None, variations=None, **kwargs):
        self.admin_variation = kwargs.pop('admin_variation', None)
        self.source_quality = kwargs.pop('source_quality', None)
        self.min_dimensions = kwargs.pop('min_dimensions', MIN_DIMENSIONS_DEFAULT)
        self.max_dimensions = kwargs.pop('max_dimensions', MAX_DIMENSIONS_DEFAULT)
        self.max_source_dimensions = kwargs.pop('max_source_dimensions', MAX_SOURCE_DIMENSIONS_DEFAULT)
        self.max_size = kwargs.pop('max_size', MAX_SIZE_DEFAULT)

        self.crop_area = kwargs.pop('crop_area', False)

        # Форматируем вариации
        self._variations = variations
        self.variations = format_variations(variations)

        # Аспекты кропа. По умолчанию будет использоваться первый.
        # Остальные можно использовать с помощью JS
        self._aspects = kwargs.pop('aspects', ())
        self.aspects = format_aspects(self._aspects, self._variations)

        super().__init__(verbose_name, name, **kwargs)

    def check(self, **kwargs):
        errors = super().check(**kwargs)
        errors.extend(self._check_min_dimensions_attribute(**kwargs))
        errors.extend(self._check_max_dimensions_attribute(**kwargs))
        errors.extend(self._check_max_source_dimensions_attribute(**kwargs))
        errors.extend(self._check_variations_attribute(**kwargs))
        errors.extend(self._check_admin_variation_attribute(**kwargs))
        errors.extend(self._check_aspects_attribute(**kwargs))
        return errors

    def _check_min_dimensions_attribute(self, **kwargs):
        if not is_size(self.min_dimensions):
            return [
                checks.Error(
                    'min_dimensions should be a tuple of 2 non-negative numbers',
                    obj=self
                )
            ]
        else:
            return []

    def _check_max_dimensions_attribute(self, **kwargs):
        if not is_size(self.max_dimensions):
            return [
                checks.Error(
                    'max_dimensions should be a tuple of 2 non-negative numbers',
                    obj=self
                )
            ]
        else:
            return []

    def _check_max_source_dimensions_attribute(self, **kwargs):
        if not is_size(self.max_source_dimensions):
            return [
                checks.Error(
                    'max_source_dimensions should be a tuple of 2 non-negative numbers',
                    obj=self
                )
            ]
        else:
            return []

    def _check_variations_attribute(self, **kwargs):
        if not self._variations:
            return [
                checks.Error(
                    'variations is required',
                    obj=self
                )
            ]
        elif not isinstance(self._variations, dict):
            return [
                checks.Error(
                    'variations should be a dict',
                    obj=self
                )
            ]

        errors = []
        errors.extend(check_variations(self._variations, self))
        return errors

    def _check_admin_variation_attribute(self, **kwargs):
        if not self.admin_variation:
            return [
                checks.Error(
                    'admin_variation is required',
                    obj=self
                )
            ]
        elif self.admin_variation not in self._variations:
            return [
                checks.Error(
                    'admin_variation "%s" not found in variations' % self.admin_variation,
                    obj=self
                )
            ]
        else:
            return []

    def _check_aspects_attribute(self, **kwargs):
        if self._aspects:
            return []

        errors = []
        aspects = self._aspects if isinstance(self._aspects, tuple) else (self._aspects,)
        for aspect in aspects:
            try:
                float(aspect)
            except (TypeError, ValueError):
                if not isinstance(aspect, str):
                    errors.append(
                        checks.Error(
                            'aspect can be only float or str instance',
                            obj=self
                        )
                    )
                elif aspect not in self._variations:
                    errors.append(
                        checks.Error(
                            'aspect variation not found: %r' % aspect,
                            obj=self
                        )
                    )
                elif not all(d > 0 for d in self._variations[aspect]['size']):
                    errors.append(
                        checks.Error(
                            'aspect should point to full-filled size: %r' % aspect,
                            obj=self
                        )
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
            'min_dimensions': self.min_dimensions,
            'max_dimensions': self.max_dimensions,
            'aspects': self.aspects,
        }
        defaults.update(kwargs)
        return super().formfield(**defaults)

    def get_variations(self, instance):
        """ Возвращает настройки вариаций """
        return self.variations

    def get_source_quality(self, instance):
        """ Возвращает качество исходника, если он сохраняется через PIL """
        return self.source_quality or DEFAULT_SOURCE_QUALITY

    def get_variation_quality(self, instance, variation):
        """ Возвращает качество картинок вариаций по умолчанию """
        return variation.get('quality') or DEFAULT_VARIATION_QUALITY

    def get_min_dimensions(self, instance):
        """ Возвращает минимальные размеры картинки для загрузки """
        return self.min_dimensions

    def get_max_dimensions(self, instance):
        """ Возвращает максимальные размеры картинки для загрузки """
        return self.max_dimensions

    def get_max_source_dimensions(self, instance):
        """ Возвращает максимальные размеры исходника картинки """
        return self.max_source_dimensions

    def get_max_size(self, instance):
        """ Возвращает максимальный вес картинки для загрузки """
        return self.max_size

    def build_source_name(self, instance, ext):
        """ Построение имени файла исходника """
        return '%s_%s.%s' % (self.name, instance.pk, ext.lower())

    def post_save(self, instance, is_uploaded=False, croparea=None, **kwargs):
        """ Обработчик сигнала сохранения экземпляра модели """
        # Если не загрузили новый файл и не обрезали старый исходник - выходим
        if not is_uploaded and not croparea:
            return

        field_file = getattr(instance, self.name)
        if not field_file or not field_file.exists():
            return

        field_file.croparea = croparea

        draft_size = None
        try:
            field_file.open()
            source_img = Image.open(field_file)
            source_format = source_img.format
            source_info = source_img.info

            if is_uploaded:
                draft_size = limited_size(source_img.size, self.get_max_source_dimensions(instance))
                if draft_size is not None:
                    old_width = source_img.size[0]
                    draft = source_img.draft(None, draft_size)
                    if draft is None:
                        source_img = source_img.resize(draft_size, Image.LINEAR)

                    # Учитываем изменение размера исходника на области обрезки
                    if field_file.croparea:
                        decr_relation = old_width / source_img.size[0]
                        croparea = tuple(round(coord / decr_relation) for coord in field_file.croparea)
                        field_file.croparea = croparea

            source_img.load()
        finally:
            field_file.close()

        update_fields = {}

        # Сохраняем исходник
        if is_uploaded:
            source_path = self._save_source_file(
                instance, source_img, source_format,
                draft_size=draft_size, **source_info
            )
            update_fields[self.attname] = source_path

        if croparea and self.crop_field:
            update_fields[self.crop_field] = croparea

        self.update_instance(instance, **update_fields)

        # Обрабатываем вариации
        self.build_variation_images(instance, source_img, source_format, croparea=field_file.croparea)
