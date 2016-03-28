from django.template import loader
from django.forms.utils import flatatt
from django.shortcuts import resolve_url
from django.core.urlresolvers import NoReverseMatch


def set_active(menulist, request):
    """
        Установка активного пункта меню.
    """
    for item in menulist:
        if item.child_count:
            set_active(item, request)

        if isinstance(item, MenuItem) and item.is_active(request):
            item.active_branch(True)


class MenuListMixin:
    _parent = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._childs = []

    def __iter__(self):
        return iter(self._childs)

    def __getitem__(self, index):
        return self._childs[index]

    @property
    def parent(self):
        return self._parent

    def child_count(self):
        return len(self._childs)

    def append(self, *items):
        for item in items:
            item._parent = self
        self._childs.extend(items)
        return self

    def clear(self):
        self._childs.clear()
        return self

    def insert(self, index, item):
        item._parent = self
        self._childs.insert(index, item)
        return self

    def pop(self, index):
        return self._childs.pop(index)

    def from_config(self, config, item_class):
        """ Создание пунктов меню из списка """
        self.clear()
        for item in config:
            item_childs = item.pop('childs', [])

            menu_item = item_class(**item)

            if item_childs:
                menu_item.from_config(item_childs, item_class)

            self.append(menu_item)


class MenuItem(MenuListMixin):
    """
        Класс пункта меню.

        Пример создания пункта:
            item = MenuItem('Yandex', 'http://yandex.ru', attrs={
                'target': '_blank',
                'class': 'my-menu red-item'
            })
    """
    _active = False

    def __init__(self, title, url, url_args=(), url_kwargs=None, attrs=None, is_active=None):
        super().__init__()

        self.title = str(title)

        url_kwargs = url_kwargs or {}
        try:
            self.link = resolve_url(url, *url_args, **url_kwargs)
        except NoReverseMatch:
            self.link = str(url)

        self._is_active = is_active
        self.attrs = attrs or {}
        self.classes = self.attrs.pop('class', '')

    def __repr__(self):
        return 'MenuItem({0.title!r}, {0.link!r})'.format(self)

    @property
    def flat_attrs(self):
        return flatatt(self.attrs) if self.attrs else ''

    def is_active(self, request):
        """ Является ли пункт активным """
        if callable(self._is_active):
            return self._is_active(request)
        else:
            return request.path_info.startswith(self.link)

    def active_branch(self, value):
        """ Распростронение активности вверх по ветке """
        self.active = value
        if self.parent and isinstance(self.parent, MenuItem):
            self.parent.active_branch(value)

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, value):
        self._active = bool(value)


class Menu(MenuListMixin):
    """
        Класс меню.
        Атрибут root является корневым уровнем пунктов меню.
    """
    item_class = MenuItem

    def __init__(self, request, config=None):
        super().__init__()
        self.request = request
        if config:
            self.from_config(config, self.item_class)

    def render(self, template):
        """ Рендер шаблона """
        set_active(self, self.request)
        return loader.render_to_string(template, {
            'items': self
        })
