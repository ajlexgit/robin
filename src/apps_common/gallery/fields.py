from django.db import models
from django.db.models import signals
from django.utils.image import Image
from django.core.files.base import ContentFile
from libs.variation_field import *
from .formfields import GalleryFormField


class GalleryImageFieldFile(VariationImageFieldFile):

    def save(self, name, content, save=True):
        setattr(self.instance, '_{}_new_file'.format(self.field.name), True)
        super().save(name, content, save)


class GalleryImageField(VariationImageField):
    attr_class = GalleryImageFieldFile

    def get_variations(self, instance):
        """ Возвращает настройки вариаций для их передачи в FieldFile """
        if not instance.content_type_id:
            # fix для loaddata
            return {}
        return instance.variations()

    def get_source_quality(self, instance):
        """ Возвращает качество исходника, если он сохраняется через PIL """
        return instance.SOURCE_QUALITY

    def get_default_quality(self, instance):
        """ Возвращает качество картинок вариаций по умолчанию """
        return instance.DEFAULT_QUALITY

    def get_min_dimensions(self, instance):
        """ Возвращает минимальные размеры картинки для загрузки """
        return instance.MIN_DIMENSIONS

    def get_max_dimensions(self, instance):
        """ Возвращает максимальные размеры картинки для загрузки """
        return instance.MAX_DIMENSIONS

    def get_max_size(self, instance):
        """ Возвращает максимальный вес картинки для загрузки """
        return instance.MAX_SIZE

    @staticmethod
    def build_source_name(instance, ext):
        """ Построение имени файла исходника """
        return '%04d.%s' % (instance.pk, ext.lower())

    def post_save(self, instance, **kwargs):
        """ Обработчик сигнала сохранения экземпляра модели """
        field_file = getattr(instance, self.name)
        if not field_file or not field_file.exists():
            return

        new_file_attrname = '_{}_new_file'.format(self.name)

        # Флаг, что загружен новый файл
        new_file_uploaded = getattr(instance, new_file_attrname, False)

        # Если не загрузили новый файл - выходим
        if not new_file_uploaded:
            return

        # Удаляем временные атрибуты
        if hasattr(instance, new_file_attrname):
            delattr(instance, new_file_attrname)

        draft_size = None
        try:
            field_file.open()
            source_img = Image.open(field_file)
            source_format = source_img.format
            source_info = source_img.info

            if new_file_uploaded:
                draft_size = limited_size(source_img.size, instance.MAX_SOURCE_DIMENSIONS)
                if draft_size is not None:
                    draft = source_img.draft(None, draft_size)
                    if draft is None:
                        source_img = source_img.resize(draft_size, Image.LINEAR)

            source_img.load()
        finally:
            field_file.close()

        # Путь к исходнику
        out_name = self.build_source_name(instance, source_format)
        source_path = self.generate_filename(instance, out_name)
        source_path = self.storage.get_available_name(source_path)

        # Сохраняем исходник
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

        # Записываем путь к исходнику в БД
        setattr(instance, self.attname, source_path)
        instance.save()

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
        }
        defaults.update(kwargs)
        return super().formfield(**defaults)

    def pre_delete(self, instance=None, **kwargs):
        """ Удаление галереи при удалении сущности """
        gallery = getattr(instance, self.name)
        if gallery:
            gallery.delete()
