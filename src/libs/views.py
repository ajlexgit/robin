import os
from django.contrib import admin
from django.template import loader
from django.utils.translation import get_language
from django.views.decorators.http import condition
from django.core.exceptions import ImproperlyConfigured
from django.views.generic.base import View, TemplateResponseMixin


class DecoratableViewMixin:
    """
        Представление, добавляющее методы before_METHOD,
        выполняющиеся перед вызовом соответствующего обработчика.

        Эти методы могут устанавлисать данные, необходимые
        для декораторов, таких как condition.
    """
    method = ''

    def get_handler(self, request):
        return getattr(self, self.method, None)

    def dispatch(self, request, *args, **kwargs):
        self.method = request.method.lower()
        if not self.method in self.http_method_names:
            return self.http_method_not_allowed(request, *args, **kwargs)

        handler = self.get_handler(request)
        if not callable(handler):
            return self.http_method_not_allowed(request, *args, **kwargs)

        # метод, вызываемый перед вызовом обработчика
        before_handler = getattr(self, 'before_%s' % handler.__name__, None)
        if before_handler:
            before_handler(request, *args, **kwargs)

        return handler(request, *args, **kwargs)


class AdminViewMixin:
    """
        Миксина для админской вьюхи
    """
    def get_handler(self, request):
        handler = super().get_handler(request)
        if handler:
            handler = admin.site.admin_view(handler)
        return handler


class LanguageViewMixin:
    """
        Миксина, добавляющая метод для поиска специальных языковых шаблонов.

        Например поиск шаблона "module/page.html" превращается в поиск
        первого из шаблонов ["module/ru/page.html", "module/page.html"].

        Миксина должна быть перед TemplateResponseMixin (если она есть).
    """
    def get_template_names(self, template=None):
        original_template = template or getattr(self, 'template_name', None)
        if original_template is None:
            raise ImproperlyConfigured("LanguageViewMixin requires either a definition of 'template_name'")

        lang = get_language()
        parts = os.path.split(original_template)
        lang_template = os.path.join(parts[0], lang, *parts[1:])
        return [lang_template, original_template]


class StringRenderMixin(LanguageViewMixin):
    """
        Представление, добавляющее метод render_to_string для
        рендеринга шаблона в строку.

        Миксина должна быть перед TemplateResponseMixin (если она есть).
    """
    def render_to_string(self, template, context=None, using=None):
        template_names = self.get_template_names(template)
        new_template = loader.select_template(template_names, using=using)

        request = getattr(self, 'request', None)
        return new_template.render(context, request)


class TemplateExView(StringRenderMixin, DecoratableViewMixin, TemplateResponseMixin, View):
    """
        Расширенная версия TemplateView:
        1) Позволяет рендерить шаблон в строку
        2) Позволяет установить кэширование в браузере для GET-страницы
           путем задания методов last_modified и/или etag.

        Пример:
            class IndexView(TemplateExView):
                config = None
                template_name = 'module/index.html'

                def before_get(self, request, *args, **kwargs):
                    self.config =  ModuleConfig.get_solo()

                def last_modified(self, *args, **kwargs):
                    return self.config.updated

                def get(self, request):
                    return self.render_to_response({
                        'config': self.config,
                    })
    """
    def last_modified(self, *args, **kwargs):
        return None

    def etag(self, *args, **kwargs):
        return None

    def get_handler(self, request):
        handler = super().get_handler(request)
        if handler and self.method == 'get':
            return condition(
                last_modified_func=self.last_modified,
                etag_func=self.etag,
            )(handler)
        else:
            return handler
