"""
    СЕО-модуль.

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

    Настройки:
        settings.py:
            SEO_TITLE_JOIN_WITH = ''

    Пример:
        views.py:
            ...
            request.seo.set(title='Clients')
            ...

        template.html:
            ...
            <title>{{ seo.title }}</title>
            <meta name="keywords" content="{{ seo.keywords }}" />
            <meta name="description" content="{{ seo.description }}" />
            ...

    Добавление блока SEO к админке объекта:
        admin.py:
            ...
            class PageAdmin(SeoModelAdminMixin, ModelAdminMixin, SingletonModelAdmin):
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

"""
default_app_config = 'seo.apps.Config'