"""
    СЕО-модуль.

    Позволяет указывать значения title, keywords, desription и др. для экземпляров
    моделей и для сайта в целом.

    Поддерживает указание некоторых OpenGraph-метаданных.

    Необязательные настройки:
        # Если не пустая строка - она будет объединять части дэка заголовков.
        # Если пустая строка - будет выведен только первый элемент дэка
        SEO_TITLE_JOIN_WITH = ' | '

    Подключение к модели:
        page/admin.py:
            ...
            class PageAdmin(SeoModelAdminMixin, admin.ModelAdmin):
                fieldsets = (
                    (None, {
                        'classes': ('suit-tab', 'suit-tab-general'),
                        ...,
                    }),
                )
                suit_form_tabs = (
                    ('general', _('General')),
                )
            ...

    Счетчики и SEO-текст:
        {% load seo %}
        <head>
            ...
            {% seo_counters 'head' %}
        </head>
        <body>
            {% seo_counters 'body_top' %}
            ...

            {% seo_block entity %}

            ...
            {% seo_counters 'body_bottom' %}
        </body>

        Если нет возможности указать entity для seo_block, можно указать
        параметр seodata в request:
            from seo import Seo
            request.seodata = Seo.get_for(entity)

        P.S: Если в представлениях используется алиас set_data,
        то ни entity ни request.seodata устанавливать не нужно.


    Пример:
        views.py:
            from seo import Seo

            # Простейшая установка SEO-данных из объекта SeoData, привязанного к entity:
                seo = Seo()
                seo.set_data(instance, defaults={
                    'title': entity.title,
                    'keywords': 'Default keywords',
                })
                seo.save(request)

            # Установка цепочки заголовков:
                seo = Seo()
                seo.set_title(shop, default=shop.title)
                seo.set_title(category, default=category.title)
                seo.set_data(product, defaults={
                    'title': product.title,
                })
                seo.save(request)

        template.html:
            ...
            <title>{{ request.seo.title }}</title>
            <meta name="keywords" content="{{ request.seo.keywords }}" />
            <meta name="description" content="{{ request.seo.description }}" />
            ...

"""

from .seo import Seo

__all__ = ['Seo']

default_app_config = 'seo.apps.Config'
