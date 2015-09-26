from django.db import models
from django.db.models import signals
from django.utils.image import Image
from libs.variation_field import *
from .formfields import GalleryFormField


class GalleryImageField(VariationImageField):

    def get_variations(self, instance):
        """ Возвращает настройки вариаций для их передачи в FieldFile """
        if not instance.content_type_id:
            # fix для loaddata
            return {}
        return instance.variations()

    def get_source_quality(self, instance):
        """ Возвращает качество исходника, если он сохраняется через PIL """
        return instance.SOURCE_QUALITY

    def get_variation_quality(self, instance, variation):
        """ Возвращает качество картинок вариаций по умолчанию """
        return variation.get('quality') or instance.DEFAULT_QUALITY

    def get_min_dimensions(self, instance):
        """ Возвращает минимальные размеры картинки для загрузки """
        return instance.MIN_DIMENSIONS

    def get_max_dimensions(self, instance):
        """ Возвращает максимальные размеры картинки для загрузки """
        return instance.MAX_DIMENSIONS

    def get_max_source_dimensions(self, instance):
        """ Возвращает максимальные размеры исходника картинки """
        return instance.MAX_SOURCE_DIMENSIONS

    def get_max_size(self, instance):
        """ Возвращает максимальный вес картинки для загрузки """
        return instance.MAX_SIZE

    @staticmethod
    def build_source_name(instance, ext):
        """ Построение имени файла исходника """
        return '%04d.%s' % (instance.pk, ext.lower())

    def post_save(self, instance, is_uploaded=False, **kwargs):
        """ Обработчик сигнала сохранения экземпляра модели """
        if not is_uploaded:
            return

        field_file = getattr(instance, self.name)
        if not field_file or not field_file.exists():
            return

        draft_size = None
        try:
            field_file.open()
            source_img = Image.open(field_file)
            source_format = source_img.format
            source_info = source_img.info

            if is_uploaded:
                draft_size = limited_size(source_img.size, self.get_max_source_dimensions(instance))
                if draft_size is not None:
                    draft = source_img.draft(None, draft_size)
                    if draft is None:
                        source_img = source_img.resize(draft_size, Image.LINEAR)

            source_img.load()
        finally:
            field_file.close()

        source_path = self._save_source_file(
            instance, source_img, source_format,
            draft_size=draft_size, **source_info
        )

        self.update_instance(instance, **{
            self.attname: source_path,
        })

        # Обрабатываем вариации
        self.build_variation_images(instance, source_img, source_format)


class GalleryVideoLinkPreviewField(VariationImageField):

    def validate(self, value, model_instance):
        if value:
            self.validate_type(value, model_instance)

        super(VariationImageField, self).validate(value, model_instance)

    def get_variations(self, instance):
        """ Возвращает настройки вариаций для их передачи в FieldFile """
        if not instance.content_type_id:
            # fix для loaddata
            return {}
        return instance.variations()

    def get_source_quality(self, instance):
        """ Возвращает качество исходника, если он сохраняется через PIL """
        return instance.SOURCE_QUALITY

    def get_variation_quality(self, instance, variation):
        """ Возвращает качество картинок вариаций по умолчанию """
        return variation.get('quality') or instance.DEFAULT_QUALITY

    @staticmethod
    def build_source_name(instance, ext):
        """ Построение имени файла исходника """
        return '%04d.%s' % (instance.pk, ext.lower())

    def post_save(self, instance, is_uploaded=False, **kwargs):
        """ Обработчик сигнала сохранения экземпляра модели """
        if not is_uploaded:
            return

        field_file = getattr(instance, self.name)
        if not field_file or not field_file.exists():
            return

        try:
            field_file.open()
            source_img = Image.open(field_file)
            source_format = source_img.format
            source_info = source_img.info
            source_img.load()
        finally:
            field_file.close()

        self._save_source_file(instance, source_img, source_format, **source_info)

        # Обрабатываем вариации
        self.build_variation_images(instance, source_img, source_format)


class GalleryField(models.OneToOneField):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('on_delete', models.SET_NULL)
        super().__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name, virtual_only=False):
        super().contribute_to_class(cls, name, virtual_only)
        signals.pre_delete.connect(self.pre_delete, sender=cls)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': GalleryFormField,
            'related_model': self.rel.to,
        }
        defaults.update(kwargs)
        return super().formfield(**defaults)

    def pre_delete(self, instance=None, **kwargs):
        """ Удаление галереи при удалении сущности """
        gallery = getattr(instance, self.name)
        if gallery:
            gallery.delete()
