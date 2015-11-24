from django.template import Library
from django.utils.translation import ugettext_lazy as _
from ..menu import Menu, MenuItem

register = Library()


@register.simple_tag(takes_context=True)
def main_menu(context, template='menu/menu.html'):
    """ Главное меню """
    request = context.get('request')
    if not request:
        return ''

    menu = Menu(request)
    menu.append(
        MenuItem(_('News'), '#'),
        MenuItem(_('Articles'), '#'),
        MenuItem(_('Contacts'), 'contacts:index'),
    )
    return menu.render(template)
