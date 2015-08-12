from django.template import loader, Context, RequestContext
from django.views.generic.base import TemplateResponseMixin, View


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
    """
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
