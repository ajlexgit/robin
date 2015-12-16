from django.shortcuts import redirect
from django.template import loader, RequestContext
from django.utils.translation import ugettext_lazy as _
from seo import Seo
from libs.email import send
from libs.views import TemplateExView
from .models import ContactsConfig, MessageReciever
from .forms import ContactForm


class IndexView(TemplateExView):
    config = None
    template_name = 'contacts/index.html'

    def before_get(self, request):
        self.config = ContactsConfig.get_solo()

    def before_post(self, request):
        self.config = ContactsConfig.get_solo()

    def get(self, request):
        form = ContactForm()

        # SEO
        seo = Seo()
        seo.set_data(self.config, defaults={
            'title': _('Contacts')
        })
        seo.save(request)

        return self.render_to_response({
            'config': self.config,
            'form': form,
        })

    def post(self, request):
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            recievers = MessageReciever.objects.all().values_list('email', flat=True)
            send(request, recievers,
                subject=_('Message from {domain}'),
                template='contacts/mails/email.html',
                context={
                    'data': form.cleaned_data,
                }
            )

            return redirect('contacts:index')
        else:
            return self.render_to_response({
                'config': self.config,
                'form': form,
            })


def contact_block_render(request, block):
    context = RequestContext(request, {
        'block': block,
    })
    return loader.render_to_string('contacts/block.html', context_instance=context)

