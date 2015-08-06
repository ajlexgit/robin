"""
    Модуль, позволяющий создавать HTML-блоки определенных типов,
    привязывать их к конкретным страницам и менять порядок их следования
    через интерфейс администратора.

    1. Для каждого блока должна быть создана модель, зарегистрированная в админке.
    2. Для каждого блока должна быть создана функция рендеринга.
    3. Добавить inline в админскую модель страницы, к которой нужно присоединять блоки

    Пример:
        # models.py

            from attachable_blocks import AttachableBlock, register_block

            @register_block(name='My super blocks')
            class MyBlock(AttachableBlock):
                pass


        # views.py

            from attachable_blocks import register_block_renderer
            from .models import MyBlock

            @register_block_renderer(MyBlock)
            def my_block_render(request, block):
                ...


        # admin.py

            from attachable_blocks import AttachableBlockRefTabularInline
            from .models import MyBlock

            class MyPageBlockRefInline(AttachableBlockRefTabularInline):
                suit_classes = 'suit-tab suit-tab-blocks'

            ...

            @admin.register(MyBlock)
            class MyBlockAdmin(admin.ModelAdmin):
                list_display = ('__str__', 'visible')

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

from .models import AttachableBlock, AttachableBlockRef
from .register import register_block, register_block_renderer
from .admin import AttachableBlockRefTabularInline, AttachableBlockRefStackedInline