from django.utils.translation import ugettext_lazy as _
from libs.cache import cached
from .base import Menu, MenuItem


@cached(time=5 * 60)
def get_main_menu():
    """ Главное меню """
    menu = Menu()
    menu.append(
        MenuItem(
            title=_('Blog'),
            url='blog:index',
        ),
        MenuItem(
            title=_('Contacts'),
            url='contacts:index',
        ),
    )
    return menu

