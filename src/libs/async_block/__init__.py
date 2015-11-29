"""
    Модуль для блоков, загружаемых через AJAX при открытии страницы.

    Зависит от:
        libs.views_ajax

    Требуется подключить скрипт:
        async_block/js/async_block.js

    Пример использования:
        # views.py
            class AsyncHeader(AsyncBlockView):
                allowed = ('id', )

                def render(self, request, id=''):
                    return '(ID %s)' % id

        # urls.py
            url(r'^async/$', views_ajax.AsyncHeader.as_view(), name='async'),

        # template.html
            {% load async_block %}
            ...
            {% if request.user.is_staff %}
                {% async_block 'module:async' id=post.id %}
            {% else %}
                {% sync_block 'module:async' id=post.id %}
            {% endif %}
"""

from .views import AsyncBlockView

__all__ = ['AsyncBlockView']