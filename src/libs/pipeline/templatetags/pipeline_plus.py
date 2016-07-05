import os
import re
import codecs
import hashlib
from django.conf import settings
from django.core.cache import cache
from django.utils.safestring import mark_safe
from django.template import Library, TemplateSyntaxError, loader
from django.contrib.staticfiles.storage import staticfiles_storage
from pipeline.templatetags import pipeline
from pipeline.utils import guess_type
from pipeline.compressors import URL_DETECTOR

register = Library()
NON_REWRITABLE_URL = re.compile(r'^(#|http:|https:|data:|//|/)')


class StylesheetNode(pipeline.StylesheetNode):
    """
        Добавлено время изменения файла
    """
    def render_css(self, package, path):
        template_name = package.template_name or "pipeline/css_default.html"
        modified = staticfiles_storage.modified_time(path).timestamp()
        context = package.extra_context
        context.update({
            'type': guess_type(path, 'text/css'),
            'url': mark_safe(staticfiles_storage.url(path)),
            'modified': int(modified),
        })
        return loader.render_to_string(template_name, context)


class InlineStylesheetNode(pipeline.StylesheetNode):
    def render_css(self, package, path):
        cache_key = ':'.join((
            self.name,
            str(staticfiles_storage.modified_time(path).timestamp()),
        ))
        cache_key = hashlib.md5(cache_key.encode()).hexdigest()
        if cache_key not in cache:
            cache.set(
                cache_key,
                self.render_individual_css(package, path),
                timeout=3600
            )
        return cache.get(cache_key)

    def render_individual_css(self, package, path, **kwargs):
        with codecs.open(staticfiles_storage.path(path), 'r', 'utf-8') as f:
            html = f.read()

        path_prefix = os.path.dirname(path)

        def reconstruct(match):
            asset_url = match.group(2)
            if not NON_REWRITABLE_URL.match(asset_url):
                asset_url = os.path.normpath(os.path.join(settings.STATIC_URL, path_prefix, asset_url))
            return "url(%s)" % asset_url

        html = '<style type="text/css">' + re.sub(URL_DETECTOR, reconstruct, html) + '</style>'
        return mark_safe(html)


class JavascriptNode(pipeline.JavascriptNode):
    """
        Добавлено время изменения файла
    """
    def render_js(self, package, path):
        template_name = package.template_name or "pipeline/js_default.html"
        modified = staticfiles_storage.modified_time(path).timestamp()
        context = package.extra_context
        context.update({
            'type': guess_type(path, 'text/javascript'),
            'url': mark_safe(staticfiles_storage.url(path)),
            'modified': int(modified),
        })
        return loader.render_to_string(template_name, context)


@register.tag
def inline_stylesheet(parser, token):
    try:
        tag_name, name = token.split_contents()
    except ValueError:
        raise TemplateSyntaxError(
            '%r requires exactly one argument: the name of a group in the PIPELINE.STYLESHEETS setting' %
            token.split_contents()[0])
    return InlineStylesheetNode(name)


@register.tag
def stylesheet(parser, token):
    try:
        tag_name, name = token.split_contents()
    except ValueError:
        raise TemplateSyntaxError(
            '%r requires exactly one argument: the name of a group in the PIPELINE.STYLESHEETS setting' %
            token.split_contents()[0])
    return StylesheetNode(name)


@register.tag
def javascript(parser, token):
    try:
        tag_name, name = token.split_contents()
    except ValueError:
        raise TemplateSyntaxError(
            '%r requires exactly one argument: the name of a group in the PIPELINE.JAVASVRIPT setting' %
            token.split_contents()[0])
    return JavascriptNode(name)
