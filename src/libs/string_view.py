"""
    Миксина, добавляющая в класс-потомок django.views.generic.TemplateView, 
    метод рендеринга шаблона в строку
"""
from django.template import loader, RequestContext


class RenderToStringMixin():
    def render_to_string(self, context=None, template=None):
        template = template or self.template_name
        return loader.get_template(template).render(RequestContext(self.request, context))
