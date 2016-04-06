from django.utils.html import escape
from django.shortcuts import redirect
from django.template import loader, RequestContext
from django.utils.translation import ugettext_lazy as _
from seo import Seo
from libs.email import send
from libs.views import TemplateExView
from .models import ContactsConfig, Address, MessageReciever
from .forms import ContactForm


class IndexView(TemplateExView):
    template_name = 'contacts/index.html'

    def get(self, request, *args, **kwargs):
        config = ContactsConfig.get_solo()
        form = ContactForm()

        # SEO
        seo = Seo()
        seo.set_data(config, defaults={
            'title': config.header,
        })
        seo.save(request)

        return self.render_to_response({
            'config': config,
            'addresses': Address.objects.all(),
            'form': form,
        })

    def post(self, request):
        config = ContactsConfig.get_solo()
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            referer = request.POST.get('referer', request.build_absolute_uri(request.path_info))
            message.referer = escape(referer)
            message.save()

            recievers = MessageReciever.objects.all().values_list('email', flat=True)
            send(request, recievers,
                subject=_('Message from {domain}'),
                template='contacts/mails/message.html',
                context={
                    'message': message,
                }
            )

            return redirect('contacts:index')
        else:
            return self.render_to_response({
                'config': config,
                'addresses': Address.objects.all(),
                'form': form,
            })


def contact_block_render(request, block):
    """ Рендеринг подключаемого блока контактов """
    context = RequestContext(request, {
        'block': block,
    })
    return loader.render_to_string('contacts/block.html', context_instance=context)
