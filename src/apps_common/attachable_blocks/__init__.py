"""
    Модуль, позволяющий создавать HTML-блоки определенных типов,
    привязывать их к конкретным страницам и менять порядок их следования
    через интерфейс администратора.

    Зависит от:
        libs.autocomplete

    1. Для каждого блока должна быть создана модель, зарегистрированная в админке.
    2. Для каждого блока должна быть создана функция рендеринга.
    3. Добавить inline в админскую модель страницы, к которой нужно присоединять блоки
    4. В тех случаях, когда к одной модели необходимо подключить несколько наборов блоков,
       каждая inline-модель блоков адмики должна иметь уникальное значение текстового атрибута
       set_name. Значение set_name по умолчанию равно 'default'.

    Параметр "name" у декоратора register_block позволяет задать имя типа блока,
    отображаемое в выпадающем списке в админке. По умолчанию оно равно verbose_name.

    Пример:
        # blocks/models.py:
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


        # blocks/views.py:
            def my_block_render(request, block):
                # Функция рендера блока
                context = RequestContext(request, {
                    'block': block,
                })
                return loader.render_to_string('block.html', context_instance=context)

        # page/admin.py:
            from attachable_blocks import AttachableReferenceTabularInline

            class FirstBlocksInline(AttachableReferenceTabularInline):
                # Первый набор блоков (set_name = 'default')
                verbose_name = 'My first block'
                verbose_name_plural = 'My first blocks'
                suit_classes = 'suit-tab suit-tab-blocks_1'

            class SecondBlocksInline(AttachableReferenceTabularInline):
                # Второй набор блоков
                set_name = 'second'
                verbose_name = 'My second block'
                verbose_name_plural = 'My second blocks'
                suit_classes = 'suit-tab suit-tab-blocks_2'

            @admin.register(MyPage)
            class MyPageAdmin(admin.ModelAdmin):
                ...
                inlines = (FirstBlocksInline, SecondBlocksInline, ...)
                ...
                suit_form_tabs = (
                    ...
                    ('blocks_1', _('First blocks')),
                    ('blocks_2', _('Second blocks')),
                    ...
                )

        # template.html:
            {% load attached_blocks %}

            ...
            <!-- вывод конкретного блока -->
            {% render_attachable_block block %}

            <!-- вывод блоков первого набора (set_name = 'default') -->
            {% render_attached_blocks page_object %}

            <!-- вывод блоков второго набора (set_name = 'second') -->
            {% render_attached_blocks page_object set_name='second' %}

"""

from .register import register_block
from .models import AttachableBlock, AttachableReference
from .admin import AttachableReferenceTabularInline, AttachableReferenceStackedInline

__all__ = ['register_block', 'AttachableBlock', 'AttachableBlockRef',
           'AttachableReferenceTabularInline',
           'AttachableReferenceStackedInline']