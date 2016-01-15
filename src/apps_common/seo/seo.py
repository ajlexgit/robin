from collections import deque
from django.conf import settings
from django.db.models import Model
from django.utils.html import strip_tags
from django.forms.models import model_to_dict
from django.utils.safestring import mark_safe
from django.db.models.fields.files import ImageFieldFile
from django.contrib.contenttypes.models import ContentType
from .models import SeoConfig, SeoData

TITLE_JOIN_WITH = str(getattr(settings, 'SEO_TITLE_JOIN_WITH', ' | '))

SEODATA_META = ('title', 'keywords', 'description')
SEODATA_OPENGRAPH = ('og_title', 'og_image', 'og_description')


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

    @staticmethod
    def get_or_create_for(entity):
        """ Получение или создание SeoData для объекта """
        ct = ContentType.objects.get_for_model(entity.__class__)
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
            Установка SEO-данных из экземпляра модели или словаря
        """
        if isinstance(seodata, Model):
            seodata = model_to_dict(seodata)
        elif isinstance(seodata, dict):
            pass
        else:
            raise TypeError('seodata must be an instance of Model or dict')

        for fieldname in SEODATA_META + SEODATA_OPENGRAPH:
            default = defaults.get(fieldname) if isinstance(defaults, dict) else None

            value = seodata.get(fieldname) or default
            if value is None:
                continue

            if fieldname == 'title':
                self.title_deque.appendleft(value)
            else:
                setattr(self, fieldname, value)

    def set_title(self, entity, *args, default=None):
        """
            Алиас для упрощения добавления заголовков из родительских категорий.
        """
        seodata = self.get_for(entity) or {}
        self.set(seodata, {
            'title': default,
        })

    def set_data(self, entity, *args, defaults=None):
        """
            Алиас для упрощения добавления данных, которые не нужно модифицировать
        """
        seodata = self.get_for(entity) or {}
        self.set(seodata, defaults)

        # сохраняем для передачи в request.seodata
        self._seodata = seodata

    def save(self, request):
        """ Сохранение данных в request, чтобы выводить их в шаблонах """
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

        # opengraph
        og = getattr(request, 'opengraph', None)
        if og is not None:
            og_data = {
                'url': request.build_absolute_uri(request.path_info)
            }

            og_title = getattr(self, 'og_title', None)
            if og_title:
                og_data['title'] = og_title

            og_image = getattr(self, 'og_image', None)
            if og_image:
                if isinstance(og_image, ImageFieldFile):
                    og_data['image'] = request.build_absolute_uri(og_image.url)
                elif isinstance(og_image, str) and not og_image.startswith('http'):
                    og_data['image'] = request.build_absolute_uri(og_image)

            og_description = getattr(self, 'og_description', None)
            if og_description:
                og_data['description'] = strip_tags(og_description)

            og.update(og_data)
