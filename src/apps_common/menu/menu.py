from django.template import loader
from django.forms.utils import flatatt
from django.shortcuts import resolve_url
from django.core.urlresolvers import NoReverseMatch


def add_items_from_config(config, itemlist, itemclass):
    """ Создание пунктов меню из списка """
    for item in config:
        try:
            link = resolve_url(item['url'], *item.get('url_args', ()), **item.get('url_kwargs', {}))
        except NoReverseMatch:
            link = item['url']

        menu_item = itemclass(
            item['title'],
            link,
            classes=item.get('classes', ''),
            attrs=item.get('attrs', {}),
        )

        if item.get('childs'):
            add_items_from_config(item['childs'], menu_item.childs, itemclass)

        itemlist.add(menu_item)


def set_active(itemlist, request):
    """
        Установка активного пункта меню.
    """
    for item in itemlist:
        if item.childs:
            set_active(item.childs, request)

        if item.is_active(request):
            item.active = True


class MenuItem:
    """
        Класс пункта меню.

        Пример создания пункта:
            item = MenuItem('Yandex', 'http://yandex.ru', classes='red-button underline', attrs={'target': '_blank'})
    """
    _active = False
    itemlist = None

    def __init__(self, title, link, classes='', attrs=None):
        self.title = str(title)
        self.link = str(link)
        self.classes = str(classes)
        self.attrs = flatatt(attrs) if attrs else ''
        self.childs = MenuItemList(parent_item=self)
        super().__init__()

    def __repr__(self):
        return 'MenuItem({0.title!r}, {0.link!r})'.format(self)

    def is_active(self, request):
        """ Является ли пункт активным """
        return request.path.startswith(self.link)

    @property
    def parent(self):
        if self.itemlist:
            return self.itemlist.parent_item

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, value):
        """
            Значение активности автоматически распространяется на родительские пункты
        """
        self._active = bool(value)
        if self.parent:
            self.parent.active = value


class MenuItemList:
    """
        Класс уровня меню в виде списка.
        Является обёрткой над обычным списком.
        Объекты этого класса создаются автоматически для MenuItem.childs и Menu.root
    """
    def __init__(self, parent_item=None):
        self._list = []
        self.parent_item = parent_item
        super().__init__()

    def __iter__(self):
        return iter(self._list)

    def __repr__(self):
        return repr(self._list)

    def __bool__(self):
        return len(self._list) > 0

    def __getitem__(self, index):
        return self._list[index]

    def add(self, *items):
        """
            Добавление пунктов меню.

            Пример:
                menu.root.add(
                    MenuItem('Test', '/test/').childs.add(
                        MenuItem('Subtest1', '/subtest/'),
                    ),
                    MenuItem('Test2', '/test2/'),
                )
        """
        for item in items:
            if not isinstance(item, MenuItem):
                raise TypeError('Item of MenuItemList must be an instance of MenuItem')
            item.itemlist = self
            self._list.append(item)
        return self.parent_item

    def insert(self, item, position=0):
        """
            Вставка пункта в определнную позицию.
            По умолчанию добавлется в начало.

            Пример:
                menu.root.insert(
                    MenuItem('Test3', '/test3/'),
                )
        """
        if not isinstance(item, MenuItem):
            raise TypeError('Item of MenuItemList must be an instance of MenuItem')
        item.itemlist = self
        self._list.insert(position, item)
        return self.parent_item

    def clear(self):
        self._list.clear()


class Menu:
    """
        Класс меню.
        Атрибут root является корневым уровнем пунктов меню.
    """
    root = None
    item_class = MenuItem

    def __init__(self, request, config=None):
        self.request = request
        self.root = MenuItemList()
        if config:
            add_items_from_config(config, itemlist=self.root, itemclass=self.item_class)
        super().__init__()

    def render(self, template):
        """ Рендер шаблона """
        set_active(self.root, self.request)
        return loader.render_to_string(template, {
            'items': self.root
        })
