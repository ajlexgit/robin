"""
    СЕО-модуль.

    Позволяет указывать значения title, keywords, desription и др. для экземпляров
    моделей и для сайта в целом.


    Установка:
        settings.py:
            MIDDLEWARE_CLASSES = (
                ...
                'seo.middleware.SeoMiddleware',
                ...
            )

            TEMPLATE_CONTEXT_PROCESSORS = (
                ...
                'seo.context_processors.seo',
                ...
            )

    Подключение к модели:
        admin.py:
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

    Настройки:
        settings.py:
            # Если не пуст - в качестве заголовка страницы будут все части дэка title,
            # объединенные строкой SEO_TITLE_JOIN_WITH. В противном случае,
            # заголовком будет первый элемент дэка title.
            SEO_TITLE_JOIN_WITH = ''


    Значения, введенные в объект SeoConfig являются значениями по-умолчанию для всех страниц сайта.

    Поле title является особенным, т.к. оно является дэком, который накапливает все значения, которые
    устанавливаются в качестве заголовка. Заголовком страницы становится первый (самый свежий) элемент дэка,
    если SEO_TITLE_JOIN_WITH является пустым объектом. В противном случае, все элементы дэка объединяются
    строкой SEO_TITLE_JOIN_WITH.

    В представлениях интерфейс сео-данных находится в request.seo.


    Пример:
        views.py:
            ...
            # Привязка данных, введённых для конкретной сущности:
            request.seo.set_instance(entity)

            # Изменение данных перед привязкой:
            request.seo.set_instance(entity, auto_apply=False)
            if request.seo.instance:
                request.seo.instance.title = 'New title'
                request.seo.apply_instance()

            # Добавление части заголовка и перезапись ключевых слов:
            request.seo.set(
                title = 'Clients',
                keywords = 'Sport, Box',
            )

            # Изменение последнего элемента заголовка:
            request.seo.title_deque[-1] = 'Other tail'
            ...

        template.html:
            ...
            <title>{{ seo.title }}</title>
            <meta name="keywords" content="{{ seo.keywords }}" />
            <meta name="description" content="{{ seo.description }}" />
            ...

"""
default_app_config = 'seo.apps.Config'