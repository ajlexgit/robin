"""
    СЕО-модуль.

    Зависит от:
        libs.description
        libs.storages

    1) Позволяет указывать значения title, keywords, desription
    2) Указание <link rel="canonical">
    3) Указание некоторых OpenGraph-метаданных.
    4) Управление содержимым robots.txt
    5) Добавление JS-счётчиков
    6) Специальный блок сео-текста с заголовком

    Необязательные настройки:
        # Если не пустая строка - она будет объединять части <title> страницы.
        # Если пустая строка - будет выведен только первый элемент дэка
        SEO_TITLE_JOIN_WITH = ' | '

    Подключение к модели:
        page/admin.py:
            ...
            class PageAdmin(SeoModelAdminMixin, admin.ModelAdmin):
                ...

    Установка параметров по умолчанию:
        views.py:
            from seo import Seo

            # Простейшая установка SEO-данных из объекта SeoData, привязанного к entity:
                seo = Seo()
                seo.set_data(entity, defaults={
                    'title': entity.title,
                    'og_title': entity.title,
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

            Если нет возможности указать entity для seo_block, можно указать
            параметр seodata в request:
                from seo import Seo
                request.seodata = Seo.get_for(entity)

            P.S: Если в представлениях используется метод seo.set_data(),
            то request.seodata устанавливается автоматически.

    Счетчики и SEO-текст:
        {% load seo %}

        <head>
            <title>{{ request.seo.title }}</title>
            <meta name="keywords" content="{{ request.seo.keywords }}" />
            <meta name="description" content="{{ request.seo.description }}" />
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
"""

from .seo import Seo

__all__ = ['Seo']

default_app_config = 'seo.apps.Config'
