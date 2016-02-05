from django.utils.html import escape
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
        config = ContactsConfig.get_solo()
        form = ContactForm(request.POST, request.FILES)

        if form.is_valid():
            message = form.save(commit=False)
            referer = request.POST.get('referer')
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

            return self.json_response({
                'success_message': self.render_to_string('contacts/ajax_contact_success.html', {
                    'config': config,
                })
            })
        else:
            return self.json_response({
                'errors': form.error_dict_full,
                'form': self.render_to_string('contacts/ajax_contact.html', {
                    'config': config,
                    'form': form,
                }),
            }, status=400)
