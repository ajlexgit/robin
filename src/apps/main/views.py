from django.shortcuts import redirect
from django.views.generic import TemplateView
from .models import MainPageConfig
from .forms import MainForm, InlineFormSet


class IndexView(TemplateView):
    template_name = 'main/index.html'

    def get(self, request, *args, **kwargs):
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

    def post(self, request, *args, **kwargs):
        form = MainForm(request.POST, request.FILES, prefix='main')
        formset = InlineFormSet(request.POST, request.FILES, prefix='inlines')

        form_valid = form.is_valid()
        formset_valid = formset.is_valid()
        print(form_valid, formset_valid)

        obj = form.save(commit=False)
        print('Obj', obj)
        for inline_obj in formset.save(commit=False):
            print('Inline obj', inline_obj)

        return redirect('index')


def render_first_block(request, block):
    return '<div class="block-1">%s</div>' % block.label


def render_second_block(request, block):
    return '<div class="block-2">%s</div>' % block.label
