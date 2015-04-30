from collections import deque
from django.conf import settings
from django.utils.safestring import mark_safe
from django.contrib.contenttypes.models import ContentType
from .models import SeoConfig, SeoData

TITLE_JOIN_WITH = str(getattr(settings, 'SEO_TITLE_JOIN_WITH', ''))


class Seo:
    def __init__(self):
        super().__init__()
        config = SeoConfig.get_solo()
        self._title_deque = deque((config.title, )) if config.title else deque()
        self._keywords = config.keywords
        self._description = config.description
        self._instance = None

    @property
    def title(self):
        if not self.title_deque:
            return ''
        elif TITLE_JOIN_WITH:
            return mark_safe(TITLE_JOIN_WITH.join(self.title_deque))
        else:
            return mark_safe(self.title_deque[0])

    @property
    def title_deque(self):
        return self._title_deque

    @property
    def keywords(self):
        return self._keywords

    @property
    def description(self):
        return self._description

    @property
    def instance(self):
        return self._instance

    def set(self, _dict=None, **kwargs):
        """ Установка новых сео-данных """
        data = _dict or {}
        data.update(kwargs)

        title = data.get('title')
        if title:
            self._title_deque.appendleft(str(title))

        keywords = data.get('keywords')
        if keywords:
            self._keywords = str(keywords)

        description = data.get('description')
        if description:
            self._description = str(description)

    def set_instance(self, instance, auto_apply=True):
        """ Установка объекта SeoData, привязанного к экземпляру """
        content_type = ContentType.objects.get_for_model(type(instance))
        try:
            self._instance = SeoData.objects.get(
                content_type=content_type,
                object_id=instance.pk,
            )
        except (SeoData.DoesNotExist, SeoData.MultipleObjectsReturned):
            return
        else:
            if auto_apply:
                self.apply_instance()

    def apply_instance(self):
        """ Установка сео-данных из объекта SeoData, привязанного к экземпляру """
        if self._instance:
            self.set(
                title=self._instance.title,
                keywords=self._instance.keywords,
                description=self._instance.description,
            )