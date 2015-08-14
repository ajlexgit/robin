"""
    Модуль, позволяющий создавать HTML-блоки определенных типов,
    привязывать их к конкретным страницам и менять порядок их следования
    через интерфейс администратора.

    1. Для каждого блока должна быть создана модель, зарегистрированная в админке.
    2. Для каждого блока должна быть создана функция рендеринга.
    3. Добавить inline в админскую модель страницы, к которой нужно присоединять блоки

    Пример:
        # blocks/models.py

            from attachable_blocks import AttachableBlock, register_block

            @register_block(name='My super blocks')
            class MyBlock(AttachableBlock):
                BLOCK_VIEW = 'blocks.views.my_block_render'

                title = models.CharField(_('title'), max_length=255, blank=True)

                class Meta:
                    verbose_name = _('Block')
                    verbose_name_plural = _('Blocks')

                def __str__(self):
                    return '%s (Block)' % self.title

        # blocks/admin.py
            from .models import MyBlock

            @admin.register(MyBlock)
            class MyBlockAdmin(admin.ModelAdmin):
                fieldsets = (
                    (None, {
                        'classes': ('suit-tab', 'suit-tab-general'),
                        'fields': ('label', 'visible'),
                    }),
                    (_('Private'), {
                        'classes': ('suit-tab', 'suit-tab-general'),
                        'fields': ('title', ),
                    }),
                )
                list_display = ('label', 'visible')
                suit_form_tabs = (
                    ('general', _('General')),
                )


        # blocks/views.py

            def my_block_render(request, block):
                context = RequestContext(request, {
                    'block': block,
                })
                return loader.render_to_string('block.html', context_instance=context)

        # page/admin.py

            from attachable_blocks import AttachableBlockRefTabularInline

            class MyPageBlockRefInline(AttachableBlockRefTabularInline):
                suit_classes = 'suit-tab suit-tab-blocks'

            @admin.register(MyPage)
            class MyPageAdmin(admin.ModelAdmin):
                ...
                inlines = (MyPageBlockRefInline, ...)
                ...
                suit_form_tabs = (
                    ...
                    ('blocks', _('Blocks')),
                    ...
                )

        # template.html

            {% load attached_blocks %}

            ...

            {% render_attached_blocks page_object %}
            {% render_attached_blocks page_object frame=1 %}

"""

from .register import register_block
from .models import AttachableBlock, AttachableBlockRef
from .admin import AttachableBlockRefTabularInline, AttachableBlockRefStackedInline
