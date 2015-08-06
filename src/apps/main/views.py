from django.views.generic import TemplateView
from attachable_blocks import register_block_renderer
from .models import MainPageConfig, MainBlockFirst, MainBlockSecond
from .forms import MainForm, InlineFormSet


class IndexView(TemplateView):
    template_name = 'main/index.html'

    def get(self, request):
        config = MainPageConfig.get_solo()

        form = MainForm(prefix='main')
        formset = InlineFormSet(prefix='inlines')

        # SEO
        request.seo.set_instance(config)

        # Opengraph
        request.opengraph.update({
            'url': request.build_absolute_uri(),
            'title': config.header_title,
            'image': 'http://cs307814.vk.me/v307814291/5255/5WStSQHmBpg.jpg',
            'description': config.description,
        })

        return self.render_to_response({
            'config': config,
            'form': form,
            'formset': formset,
        })


@register_block_renderer(MainBlockFirst)
def render_first_block(request, block):
    return '<div class="block-1"></div>'


@register_block_renderer(MainBlockSecond)
def render_second_block(request, block):
    return '<div class="block-2"></div>'