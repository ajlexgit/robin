from django.template import Library
from .. import options
from ..menu import Menu

register = Library()


@register.simple_tag(takes_context=True)
def main_menu(context, template='menu/menu.html'):
    """ Главное меню """
    menu = Menu(context['request'], options.MAIN_MENU)
    return menu.render(template)
