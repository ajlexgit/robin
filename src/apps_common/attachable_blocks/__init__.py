"""
    Модуль, позволяющий создавать HTML-блоки определенных типов,
    привязывать их к конкретным страницам и менять порядок их следования
    через интерфейс администратора.

    1. Для каждого блока должна быть создана модель.
    2. Для каждого блока должна быть создана функция рендеринга.
    3. Для каждой модели, у экземпляров которой должна быть
       возможность подключать блоки, нужно создать модель связи с
       блоками под именем blocks.
    4. Добавить модели блоков для админки.
    5. Добавить inline-модель связи страницы с блоками для админки.
    6. Вставить inline-модель связи страницы с блоками в поле inlines
       модели страницы в админке.

    Пример:
        # models.py

            from attachable_blocks import AttachableBlock, AttachableBlockRef, register_block


            class MyPage(models.Model):
                ...
                blocks = models.ManyToManyField(AttachableBlock,
                    symmetrical=False,
                    through='MyPageBlockRef',
                )

            class MyPageBlockRef(AttachableBlockRef):
                page = models.ForeignKey(MyPage)

                class Meta(AttachableBlockRef.Meta):
                    unique_together = ('block_model', 'page')

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
            from .models import MyBlock, MyPageBlockRef

            @admin.register(MyBlock)
            class MyBlockAdmin(admin.ModelAdmin):
                list_display = ('__str__', 'visible')

            class MyPageBlockRefInline(AttachableBlockRefTabularInline):
                model = MyPageBlockRef
                suit_classes = 'suit-tab suit-tab-blocks'

            ...

            class MyPageAdmin(admin.ModelAdmin):
                ...
                inlines = (MyPageBlockRefInline, ...)
                ...
                suit_form_tabs = (
                    ...
                    ('blocks', _('Blocks')),
                    ...
                )



    model.py:
        from blocks.models import Block, BlockRef

        class PageModel(models.Model):
            ...
            blocks = models.ManyToManyField(Block,
                verbose_name=_('blocks'),
                symmetrical=False,
                through='PageBlocks',
            )


        class PageBlocks(BlockRef):
            page = models.ForeignKey(PageModel)

            class Meta(BlockRef.Meta):
                unique_together = ('type', 'page')


    admin.py:
        from blocks.admin import BlockRefTabularInline
        from .models import PageBlocks


        class PageBlocksInline(BlockRefTabularInline):
            model = PageBlocks
            suit_classes = 'suit-tab suit-tab-blocks'


        class PageAdmin(admin.ModelAdmin):
            ...
            inlines = (..., PageBlocksInline, ...)
"""

from .models import AttachableBlock, AttachableBlockRef
from .register import get_block_subclass, register_block, register_block_renderer
from .admin import AttachableBlockRefTabularInline, AttachableBlockRefStackedInline