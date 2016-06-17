from collections import deque
from django.conf import settings
from django.db.models import Model
from django.forms.models import model_to_dict
from django.utils.safestring import mark_safe
from django.contrib.contenttypes.models import ContentType
from .models import SeoConfig, SeoData
from .metatags import Opengraph, TwitterCard


TITLE_JOIN_WITH = str(getattr(settings, 'SEO_TITLE_JOIN_WITH', ' | '))
ALLOWED_SEO_KEYS = (
    'title',
    'keywords',
    'description',
    'canonical',

    'og_title',
    'og_image',
    'og_description',

    'text_header',
    'text',
)


class TitleDescriptor:
    def __init__(self, deque_name):
        self.deque_name = deque_name

    def __get__(self, instance, owner):
        """ Возврат полного заголовка как строки """
        title_deque = instance.__dict__.get(self.deque_name, None)
        if title_deque is None:
            title_deque = deque()

        title_parts = list(filter(bool, map(str, title_deque)))
        if TITLE_JOIN_WITH:
            title = mark_safe(TITLE_JOIN_WITH.join(title_parts))
        else:
            title = mark_safe(title_parts[0]) if title_parts else ''

        return title

    def __set__(self, instance, value):
        title_deque = instance.__dict__.get(self.deque_name, None)
        if title_deque is None:
            title_deque = deque()

        title_deque.appendleft(value)
        instance.__dict__[self.deque_name] = title_deque


class Seo:
    _title_deque = None
    title = TitleDescriptor('_title_deque')

    def __init__(self, empty=False):
        super().__init__()
        self.keywords = ''
        self.description = ''
        self.canonical = ''
        self.text_header = ''
        self.text = ''

        if not empty:
            site_seoconfig = SeoConfig.get_solo()
            self.set(site_seoconfig)

    @staticmethod
    def get_for(entity):
        """ Получение SeoData для объекта """
        ct = ContentType.objects.get_for_model(type(entity))
        try:
            return SeoData.objects.get(
                content_type=ct,
                object_id=entity.pk
            )
        except (SeoData.DoesNotExist, SeoData.MultipleObjectsReturned):
            return None

    @staticmethod
    def get_or_create_for(entity):
        """ Получение или создание SeoData для объекта """
        ct = ContentType.objects.get_for_model(type(entity))
        try:
            return SeoData.objects.get(
                content_type=ct,
                object_id=entity.pk
            )
        except (SeoData.DoesNotExist, SeoData.MultipleObjectsReturned):
            return SeoData(
                content_type=ct,
                object_id=entity.pk
            )

    def set(self, seodata, defaults=None):
        """
            Установка SEO-данных из экземпляра модели SeoData или словаря.
        """
        if isinstance(seodata, Model):
            seodata = model_to_dict(seodata)
        elif isinstance(seodata, dict):
            pass
        else:
            raise TypeError('seodata must be an instance of Model or dict')

        for fieldname in ALLOWED_SEO_KEYS:
            default = defaults.get(fieldname) if isinstance(defaults, dict) else None

            value = seodata.get(fieldname) or default
            if value is None:
                continue

            setattr(self, fieldname, value)

    def set_title(self, entity, default=None):
        """
            Алиас для упрощения добавления заголовков из родительских категорий.

            Пример:
                seo = Seo()
                seo.set_title(shop, default=shop.title)
        """
        seodata = self.get_for(entity)
        title = (seodata and getattr(seodata, 'title')) or default
        if title:
            self.title = title

    def set_data(self, entity, defaults=None):
        """
            Алиас для упрощения добавления данных, которые не нужно модифицировать

            Пример:
                seo = Seo()
                seo.set_data(shop, defaults={
                    'title': shop.title,
                    'og_title': shop.title,
                })
        """
        seodata = self.get_for(entity) or {}
        self.set(seodata, defaults)

    def save(self, request):
        """ Сохранение данных в request, чтобы выводить их в шаблонах """
        # opengraph + twitter card
        social_data = {
            'url': request.build_absolute_uri(request.path_info),
            'title': getattr(self, 'og_title', None),
            'image': getattr(self, 'og_image', None),
            'description': getattr(self, 'og_description', None),
        }

        opengraph = Opengraph(request)
        opengraph.update(social_data)

        twitter_card = TwitterCard(request)
        twitter_card.update(social_data)

        # Сохранение данных в request
        request.seo = {
            'title': self.title,
            'keywords': self.keywords,
            'description': self.description,
            'canonical': self.canonical,
            'opengraph': opengraph,
            'twitter_card': twitter_card,

            'text_header': self.text_header,
            'text': self.text,
        }
