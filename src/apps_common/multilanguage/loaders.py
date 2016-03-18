import os
from django.utils.translation import get_language
from django.template.base import TemplateDoesNotExist
from django.template.loaders.base import Loader as BaseLoader
from django.template.loaders.cached import Loader as CachedLoader


class LanguageLoaderMixin:
    """
        Базовая миксина для поиска языковых шаблонов
    """
    is_usable = True
    engine = None
    loaders = ()

    def get_template_names(self, template_name, language_code):
        """ Возвращает список вариантов имени шаблона """
        parts = os.path.split(template_name)
        lang_template = os.path.join(parts[0], language_code, *parts[1:])
        return lang_template, template_name

    def get_template(self, template_name, template_dirs=None):
        """ Поиск первого существующего шаблона """
        for name in self.get_template_names(template_name, get_language()):
            for loader in self.loaders:
                try:
                    template, display_name = loader(name, template_dirs)
                except TemplateDoesNotExist:
                    pass
                else:
                    origin = self.engine.make_origin(display_name, loader, name, template_dirs)
                    return template, origin

        raise TemplateDoesNotExist(template_name)


class LanguageLoader(LanguageLoaderMixin, BaseLoader):
    """
        Загрузчик языковых шаблонов
    """
    def __init__(self, engine, loaders):
        self.loaders = engine.get_template_loaders(loaders)
        super().__init__(engine)

    def load_template(self, template_name, template_dirs=None):
        return self.get_template(template_name, template_dirs)


class LanguageCachedLoader(LanguageLoaderMixin, CachedLoader):
    """
        Загрузчик языковых шаблонов с кэшированием
    """
    def find_template(self, name, dirs=None):
        key = self.cache_key(name, dirs)

        try:
            result = self.find_template_cache[key]
        except KeyError:
            try:
                result = self.get_template(name, dirs)
            except TemplateDoesNotExist:
                result = None

        self.find_template_cache[key] = result
        if result:
            return result
        else:
            self.template_cache[key] = TemplateDoesNotExist
            raise TemplateDoesNotExist(name)
