from django.conf import settings
from django.template import loader
from django.shortcuts import redirect
from django.core.mail import send_mail, BadHeaderError
from django.contrib.sites.shortcuts import get_current_site
from django.utils.translation import ugettext_lazy as _
from seo import Seo
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
            if recievers:
                site = get_current_site(request)

                content = loader.render_to_string('contacts/mails/email.html', {
                    'data': form.cleaned_data,
                })

                try:
                    send_mail(
                        'Message from %s' % site.domain,
                        content,
                        settings.DEFAULT_FROM_EMAIL,
                        recipient_list=recievers,
                        html_message=content
                    )
                except BadHeaderError:
                    pass

            return redirect('contacts:index')
        else:
            return self.render_to_response({
                'config': self.config,
                'form': form,
            })
