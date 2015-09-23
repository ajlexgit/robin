from django.http.response import Http404
from django.views.decorators.http import condition
from django.template import loader, Context, RequestContext
from django.views.generic.base import TemplateResponseMixin, View
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


class RenderToStringMixin(TemplateResponseMixin):
    def _resolve_context(self, context, current_app=None):
        if isinstance(context, Context):
            return context
        else:
            return RequestContext(self.request, context, current_app=current_app)

    def render_to_string(self, context=None, template=None, current_app=None, dirs=None):
        template = template or self.template_name
        context = self._resolve_context(context, current_app)
        return loader.get_template(template, dirs=dirs).render(context)


class TemplateExView(RenderToStringMixin, View):
    """
        Расширенная версия TemplateView:
        1) Позволяет переопределить шаблон в методе render_to_response
        2) Позволяет рендерить шаблон в строку
        3) Позволяет задать метод get_objects, который может установить атрибуты объекту
           self. Метод автоматически перехватывает исключения ObjectDoesNotExist
           и MultipleObjectsReturned. Этот метод создан для оптимизации запросов
           при применении last_modified и etag.
        4) Позволяет установить кэширование в браузере для GET-страницы
           путем задания методов last_modified и/или etag.

        Пример:
            class IndexView(TemplateExView):
                template_name = 'contacts/index.html'

                def get_objects(self, request):
                    self.object =  ContactsConfig.get_solo()

                def last_modified(self, request):
                    return self.object.updated

                def get(self, request):
                    return self.render_to_response({
                        'config': self.object,
                    })
    """

    def get_objects(self, request, *args, **kwargs):
        pass

    def dispatch(self, request, *args, **kwargs):
        method = request.method.lower()
        if method in self.http_method_names:
            handler = getattr(self, method, self.http_method_not_allowed)

            # Декорирование GET-метода
            if method == 'get' and hasattr(self, method):
                try:
                    self.get_objects(request, *args, **kwargs)
                except (ObjectDoesNotExist, MultipleObjectsReturned):
                    raise Http404

                last_mod = getattr(self, 'last_modified', None)
                etag = getattr(self, 'etag', None)
                handler = condition(last_modified_func=last_mod, etag_func=etag)(handler)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)

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
