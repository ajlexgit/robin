from django.utils.html import escape
from django.utils.translation import ugettext_lazy as _
from django.views.generic.base import View
from libs.views_ajax import AjaxViewMixin
from libs.email import send
from .models import ContactsConfig, NotifyReceiver
from .forms import ContactForm


class ContactView(AjaxViewMixin, View):
    def get(self, request):
        config = ContactsConfig.get_solo()
        form = ContactForm()
        response = self.json_response({
            'form': self.render_to_string('contacts/ajax_contact.html', {
                'config': config,
                'form': form,
            }),
        })
        response['cache-control'] = 'public, must-revalidate, max-age=%d' % 24 * 3600
        return response

    def post(self, request):
        config = ContactsConfig.get_solo()
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            referer = request.POST.get('referer')
            message.referer = escape(referer)
            message.save()

            receivers = NotifyReceiver.objects.all().values_list('email', flat=True)
            send(request, receivers,
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
            return self.json_error({
                'errors': form.error_dict_full,
                'form': self.render_to_string('contacts/ajax_contact.html', {
                    'config': config,
                    'form': form,
                }),
            })
