"""
    СЕО-модуль.

    Позволяет указывать значения title, keywords, desription и др. для экземпляров
    моделей и для сайта в целом.


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
                    ('seo', _('SEO')),
                )
                suit_seo_tab = 'seo'
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
                entity_data = Seo.get_data_from(entity, defaults={
                    'title': entity.title,
                })
                seo = Seo()
                seo.set(entity_data)
                seo.save(request)


            # Установка цепочки заголовков:
                shop_data = Seo.get_data_from(shop, defaults={
                    'title': shop.title,
                })
                category_data = Seo.get_data_from(category, defaults={
                    'title': category.title,
                })
                seo = Seo()
                seo.set({
                    'title': shop_data.get('title')
                })
                seo.set(category_data)
                seo.save(request)

            # Вышеприведенная ситуация случается часто, поэтому введены
            # алиасы set_title и set_data для сокращения кода:
                seo = Seo()
                seo.set_title(shop, default=shop.title)
                seo.set_data(category, defaults={
                    'title': category.title,
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
