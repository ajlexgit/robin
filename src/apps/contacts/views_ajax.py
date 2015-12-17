from django.utils.translation import ugettext_lazy as _
from libs.views import TemplateExView
from libs.views_ajax import AjaxViewMixin
from libs.email import send
from .models import ContactsConfig, MessageReciever
from .forms import ContactForm


class ContactView(AjaxViewMixin, TemplateExView):
    def get(self, request):
        form = ContactForm()
        config = ContactsConfig.get_solo()

        return self.render_to_response({
            'config': config,
            'form': form,
        }, template='contacts/ajax_contact.html')

    def post(self, request):
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            recievers = MessageReciever.objects.all().values_list('email', flat=True)
            send(request, recievers,
                subject=_('Message from {domain}'),
                template='contacts/mails/email.html',
                context={
                    'data': form.cleaned_data,
                    'referer': request.POST.get('referer'),
                }
            )

            return self.json_response()
        else:
            config = ContactsConfig.get_solo()
            return self.json_response({
                'errors': form.error_dict_full,
                'form': self.render_to_string('contacts/ajax_contact.html', {
                    'config': config,
                    'form': form,
                }),
            })
