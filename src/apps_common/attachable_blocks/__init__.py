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

        # blocks/admin.py
            from .models import MyBlock

            @admin.register(MyBlock)
            class MyBlockAdmin(admin.ModelAdmin):
                list_display = ('__str__', 'visible')


        # blocks/views.py

            def my_block_render(request, block):
                ...

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

"""

from .register import register_block
from .models import AttachableBlock, AttachableBlockRef
from .admin import AttachableBlockRefTabularInline, AttachableBlockRefStackedInline