from django.shortcuts import redirect
from seo import Seo
from libs.views import TemplateExView
from .models import MainPageConfig, ClientFormModel
from .forms import MainForm, InlineFormSet


class IndexView(TemplateExView):
    config = None
    template_name = 'main/index.html'

    def before_get(self, request):
        self.config = MainPageConfig.get_solo()

    def get(self, request):
        # SEO
        seo = Seo()
        seo.set_data(self.config)
        seo.save(request)

        # Opengraph
        request.opengraph.update({
            'url': request.build_absolute_uri(),
            'title': self.config.header_title,
            'image': 'http://cs307814.vk.me/v307814291/5255/5WStSQHmBpg.jpg',
            'description': self.config.description,
        })

        return self.render_to_response({
            'config': self.config,
        })


def render_first_block(request, block):
    return '<div class="block-1">%s</div>' % block.label


def render_second_block(request, block):
    return '<div class="block-2">%s</div>' % block.label


class FormsView(TemplateExView):
    config = None
    template_name = 'main/forms.html'

    def before_get(self, request):
        self.config = MainPageConfig.get_solo()

    def get(self, request):
        form_obj = ClientFormModel.objects.first()
        form = MainForm(instance=form_obj, prefix='main')
        formset = InlineFormSet(instance=form_obj, prefix='inlines')

        form.load_from_session(request)
        form.remove_from_session(request)

        # formset.load_from_session(request)
        # formset.remove_from_session(request)

        return self.render_to_response({
            'config': self.config,
            'form': form,
            'formset': formset,
        })

    def post(self, request):
        form_obj = ClientFormModel.objects.first()
        form = MainForm(request.POST, request.FILES, instance=form_obj, prefix='main')
        formset = InlineFormSet(request.POST, request.FILES, instance=form_obj, prefix='inlines')

        form_valid = form.is_valid()
        formset_valid = formset.is_valid()

        if form_valid and formset_valid:
            form.remove_from_session(request)
            # formset.remove_from_session(request)

            form.save()
            formset.save()
        else:
            form.save_to_session(request)
            # formset.save_to_session(request)

        return redirect('forms')
