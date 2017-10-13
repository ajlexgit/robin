from django.utils.translation import ugettext_lazy as _
from .base import Menu, MenuItem


def main(request):
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
         MenuItem(
            title=_('Contacts'),
            url='contacts:index',
        ),
    )
    return menu

