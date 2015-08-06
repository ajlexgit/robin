"""
    Модуль, позволяющий создавать HTML-блоки определенных типов,
    привязывать их к конкретным страницам и менять порядок их следования
    через интерфейс администратора.

    1. Для каждого блока должна быть создана модель:
            from attached_blocks import AttachableBlock, register_block

            # если name не указан, будет использован verbose_name_plural
            @register_block(name='My super blocks')
            class MyBlock(AttachableBlock):
                pass

    2. Для каждого блока должна быть создана функция рендеринга:
            from attached_blocks import register_block_renderer

            @register_block_renderer
            def my_block_render(request, block):
                ...

    3. Для каждой модели, у экземпляров которой должна быть
       возможность подключать блоки, нужно создать связь:
            from attached_blocks import AttachableBlockRef

            class MyPage(models.Model):
                ...
                blocks = models.ManyToManyField(Block,
                    symmetrical=False,
                    through='PageBlocks',
                )


            class MyPageBlockRef(AttachableBlockRef):
                page = models.ForeignKey(MyPage)

                class Meta(AttachableBlockRef.Meta):
                    unique_together = ('block_model', 'page')




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

from .models import AttachableBlock
from .register import get_block_subclass, register_block, register_block_renderer