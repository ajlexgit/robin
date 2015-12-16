from django.template import Library
from django.utils.translation import ugettext_lazy as _
from blog.models import BlogConfig, BlogPost
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
        MenuItem(_('Contacts'), 'contacts:index'),
    )

    posts = BlogPost.objects.filter(visible=True)
    if posts.exists():
        menu.insert(0, MenuItem(_('Blog'), 'blog:index'))

    return menu.render(template)
