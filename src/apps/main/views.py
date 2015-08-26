from django.shortcuts import redirect
from django.views.generic import TemplateView
from .models import MainPageConfig, ClientFormModel
from .forms import MainForm, InlineFormSet


class IndexView(TemplateView):
    template_name = 'main/index.html'

    def get(self, request, *args, **kwargs):
        config = MainPageConfig.get_solo()

        form_obj = ClientFormModel.objects.first()
        form = MainForm(instance=form_obj, prefix='main')
        formset = InlineFormSet(instance=form_obj, prefix='inlines')

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
        form_obj = ClientFormModel.objects.first()
        form = MainForm(request.POST, request.FILES, instance=form_obj, prefix='main')
        formset = InlineFormSet(request.POST, request.FILES, instance=form_obj, prefix='inlines')

        form_valid = form.is_valid()
        formset_valid = formset.is_valid()

        if form_valid and formset_valid:
            form.save()
            formset.save()

        return redirect('index')


def render_first_block(request, block):
    return '<div class="block-1">%s</div>' % block.label


def render_second_block(request, block):
    return '<div class="block-2">%s</div>' % block.label
