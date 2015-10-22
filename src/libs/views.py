from django.contrib import admin
from django.views.decorators.http import condition
from django.template import loader, Context, RequestContext
from django.views.generic.base import TemplateResponseMixin, View


class DecoratableViewMixin:
    """
        Представление, добавляющее методы before_METHOD,
        выполняющиеся перед вызовом обработчика.

        Эти методы могут устанавлисать данные, необходимые
        для декораторов.
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
        before_handler = getattr(self, 'before_%s' % self.method, None)
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


class StringRenderMixin:
    """
        Представление, добавляющее метод render_to_string для
        рендеринга шаблона в строку
    """
    def render_to_string(self, template, context=None, current_app=None, dirs=None):
        if not isinstance(context, Context):
            context = RequestContext(self.request, context, current_app=current_app)

        return loader.get_template(template, dirs=dirs).render(context)


class TemplateExView(TemplateResponseMixin, StringRenderMixin, DecoratableViewMixin, View):
    """
        Расширенная версия TemplateView:
        1) Позволяет переопределить шаблон в методе render_to_response
        2) Позволяет рендерить шаблон в строку
        3) Позволяет установить кэширование в браузере для GET-страницы
           путем задания методов last_modified и/или etag.

        Пример:
            class IndexView(TemplateExView):
                template_name = 'contacts/index.html'

                def before_get(self, request, *args, **kwargs):
                    self.object =  ContactsConfig.get_solo()

                def last_modified(self, *args, **kwargs):
                    return self.object.updated

                def get(self, request):
                    return self.render_to_response({
                        'config': self.object,
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

    def render_to_response(self, context=None, template=None, dirs=None, **response_kwargs):
        template = template or self.template_name
        template = loader.get_template(template, dirs=dirs)

        response_kwargs.setdefault('content_type', self.content_type)
        return self.response_class(
            request=self.request,
            template=template,
            context=context,
            **response_kwargs
        )
