from collections import deque
from django.conf import settings
from django.db.models import Model
from django.forms.models import model_to_dict
from django.utils.safestring import mark_safe
from django.contrib.contenttypes.models import ContentType
from .models import SeoConfig, SeoData

TITLE_JOIN_WITH = str(getattr(settings, 'SEO_TITLE_JOIN_WITH', ' | '))


class Seo:
    _seodata = None

    def __init__(self, empty=False):
        super().__init__()
        self.title_deque = deque()
        self.keywords = ''
        self.description = ''

        if not empty:
            site_seoconfig = SeoConfig.get_solo()
            self.set(site_seoconfig)

    @staticmethod
    def get_for(entity):
        """ Получение SeoData для объекта """
        ct = ContentType.objects.get_for_model(entity.__class__)
        try:
            return SeoData.objects.get(
                content_type=ct,
                object_id=entity.pk
            )
        except (SeoData.DoesNotExist, SeoData.MultipleObjectsReturned):
            return None

    @classmethod
    def get_data_from(cls, entity, defaults=None):
        """
            Получение словаря данных для страницы entity
        """
        defaults = dict(defaults) if defaults else {}

        seodata = cls.get_for(entity)
        if seodata is None:
            seodata = {}
        else:
            seodata = model_to_dict(seodata)

        data = {}
        for key in ('title', 'keywords', 'description'):
            value = seodata.get(key) or defaults.get(key)
            if value is not None:
                data[key] = value

        return data

    def set(self, seodata):
        """
            Установка title, keywords и description из экземпляра модели
            или словаря
        """
        if seodata is None:
            return
        elif isinstance(seodata, Model):
            seodata = model_to_dict(seodata)
        elif isinstance(seodata, dict):
            pass
        else:
            raise TypeError('seodata must be an instance of Model or dict')

        # title
        title = seodata.get('title')
        if title is not None:
            self.title_deque.appendleft(title)

        # keywords
        keywords = seodata.get('keywords')
        if keywords is not None:
            self.keywords = str(keywords)

        # description
        description = seodata.get('description')
        if description is not None:
            self.description = str(description)

    def save(self, request):
        """ Сохранение данных в request """
        # title
        title_parts = list(filter(bool, map(str, self.title_deque)))
        if TITLE_JOIN_WITH:
            title = mark_safe(TITLE_JOIN_WITH.join(title_parts))
        else:
            title = mark_safe(title_parts[0]) if title_parts else ''

        request.seo = {
            'title': title,
            'keywords': self.keywords,
            'description': self.description,
        }

        if self._seodata and not hasattr(request, 'seodata'):
            request.seodata = self._seodata

    def set_title(self, entity, *args, default=None):
        """
            Алиас для упрощения добавления заголовков из родительских категорий.
        """
        seodata = self.get_for(entity)
        if seodata is None:
            title = ''
        else:
            title = seodata.title

        title = title or default
        if title is not None:
            self.title_deque.appendleft(title)

    def set_data(self, entity, *args, defaults=None):
        """
            Алиас для упрощения добавления данных, которые не нужно модифицировать
        """
        seodata = self.get_data_from(entity, defaults)
        self.set(seodata)

        # сохраняем для передачи в request.seodata
        self._seodata = seodata
