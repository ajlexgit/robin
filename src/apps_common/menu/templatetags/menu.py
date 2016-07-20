from django.template import Library
from django.utils.translation import ugettext_lazy as _
from ..menu import Menu, MenuItem

register = Library()


@register.simple_tag(takes_context=True)
def main_menu(context, template='menu/menu.html'):
    """ Главное меню """
    menu = Menu(request=context.get('request'))
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

    return menu.render(template)
