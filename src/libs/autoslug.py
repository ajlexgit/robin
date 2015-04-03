import pytils
from django.db import models


class AutoSlugField(models.SlugField):

    def __init__(self, *args, populate_from=None, **kwargs):
        """
            Параметры:
                populate_from - имя поля, по которому будет строиться алиас,
                                если его значение не указано явно
                separator     - разделитель префикс алиаса от суффикса.
                                (my_alias-1, my_alias-2, ...)
                default_slug  - префикс по умолчанию, если populate_from пуст.
        """
        self.populate_from = populate_from
        self.separator = kwargs.pop('separator', '-')
        self.default_slug = kwargs.pop('default_slug', 'empty')
        super(AutoSlugField, self).__init__(*args, **kwargs)

    def _get_populate_value(self, instance):
        """ Получение значения, по которому нужно строить алиас """
        if callable(self.populate_from):
            return self.populate_from(instance)
        else:
            return getattr(instance, self.populate_from)

    @staticmethod
    def _slugify(value):
        """ Функция транслитерации """
        return pytils.translit.slugify(value)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs['populate_from'] = self.populate_from
        if self.separator != '-':
            kwargs['separator'] = self.separator
        if self.default_slug != 'empty':
            kwargs['default_slug'] = self.default_slug
        return name, path, args, kwargs

    def pre_save(self, instance, add):
        manager = instance._default_manager
        qs = manager.exclude(pk=instance.pk)

        value = self.value_from_object(instance)

        # Если значение уже указано - проверяем его на уникальность и оставляем
        if value and not qs.filter((self.attname, value)).exists():
            return value

        if self.populate_from and not value:
            value = self._get_populate_value(instance)

        slug = self._slugify(value) if value else ''
        if not slug:
            slug = None if self.null else self.default_slug

        if self.unique:
            if qs.filter((self.attname, slug)).exists():
                suffix = 0
                lookup = {
                    self.attname + '__regex': r'^' + slug + self.separator + r'\d+$'
                }
                slugs = qs.filter(**lookup).values_list(self.attname, flat=True)
                if slugs:
                    prefix_len = len(slug) + len(self.separator)
                    suffix = max(map(lambda x: int(x[prefix_len:]), slugs))

                slug = slug + self.separator + str(suffix + 1)

        setattr(instance, self.attname, slug)
        return slug
