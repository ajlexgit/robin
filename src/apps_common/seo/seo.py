from django.conf import settings
from django.utils.safestring import mark_safe
from .models import SeoConfig

TITLE_JOIN_WITH = getattr(settings, 'SEO_TITLE_JOIN_WITH', '')


class Seo:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        config = SeoConfig.get_solo()
        self._title = [config.title]
        self._keywords = config.keywords
        self._description = config.description

    @property
    def title(self):
        if TITLE_JOIN_WITH:
            return mark_safe(TITLE_JOIN_WITH.join(reversed(self._title)))
        else:
            return mark_safe(self._title[-1])

    @property
    def keywords(self):
        return self._keywords

    @property
    def description(self):
        return self._description

    def set(self, _dict=None, **kwargs):
        """ Установка новых значений сео-тэгов """
        data = _dict or {}
        data.update(kwargs)

        title = data.get('title')
        if title:
            self._title.append(str(title))

        keywords = data.get('keywords')
        if keywords:
            self._keywords = str(keywords)

        description = data.get('description')
        if description:
            self._description = str(description)
