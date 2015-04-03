from django.utils.safestring import mark_safe
from . import options


class Seo:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._title = [options.DEFAULT_TITLE]
        self._keywords = options.DEFAULT_KEYWORDS
        self._description = options.DEFAULT_DESCRIPTION
    
    @property
    def title(self):
        if options.TITLE_JOIN:
            return mark_safe(options.TITLE_SEPARATOR.join(reversed(self._title)))
        else:
            return mark_safe(self._title[-1])
    
    @property
    def keywords(self):
        return self._keywords
    
    @property
    def description(self):
        return self._description

    def set(self, _dict=None, **kwargs):
        """ Установка новых значений сео-тэгов """
        data = _dict or {}
        data.update(kwargs)
        
        title = data.get('title')
        if title:
            self._title.append(str(title))
        
        keywords = data.get('keywords')
        if keywords:
            self._keywords = str(keywords)
        
        description = data.get('description')
        if description:
            self._description = str(description)
