from collections import deque
from django.conf import settings
from django.forms.models import model_to_dict
from django.utils.safestring import mark_safe
from django.contrib.contenttypes.models import ContentType
from .models import SeoConfig, SeoData

TITLE_JOIN_WITH = str(getattr(settings, 'SEO_TITLE_JOIN_WITH', ' | '))


class Seo:
    _instance = None

    def __init__(self):
        super().__init__()
        self._global = SeoConfig.get_solo()
        self._title_deque = deque((self._global.title, )) if self._global.title else deque()
        self._keywords = self._global.keywords
        self._description = self._global.description

    @property
    def title_deque(self):
        return self._title_deque

    @property
    def title(self):
        """ Возвращает заголовок страницы, объединенный TITLE_JOIN_WITH """
        if not self.title_deque:
            return ''
        elif TITLE_JOIN_WITH:
            return mark_safe(TITLE_JOIN_WITH.join(self.title_deque))
        else:
            return mark_safe(self.title_deque[0])

    @property
    def keywords(self):
        return self._keywords

    @property
    def description(self):
        return self._description

    @property
    def instance(self):
        return self._instance

    def set(self, **kwargs):
        """ Установка новых сео-данных """
        title = kwargs.get('title')
        if title:
            self._title_deque.appendleft(str(title))

        keywords = kwargs.get('keywords')
        if keywords:
            self._keywords = str(keywords)

        description = kwargs.get('description')
        if description:
            self._description = str(description)

    def set_instance(self, entity, defaults=None):
        """ Установка объекта SeoData, привязанного к экземпляру """
        defaults = dict(defaults) if defaults else {}
        content_type = ContentType.objects.get_for_model(type(entity))
        try:
            self._instance = SeoData.objects.get(
                content_type=content_type,
                object_id=entity.pk,
            )
        except (SeoData.DoesNotExist, SeoData.MultipleObjectsReturned):
            pass
        else:
            defaults.update(model_to_dict(self._instance))

        self.set(**defaults)
