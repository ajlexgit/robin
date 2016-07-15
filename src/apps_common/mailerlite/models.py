import re
from datetime import datetime
from django.db import models
from django.template import loader
from django.utils.timezone import now
from django.core.urlresolvers import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.translation import ugettext_lazy as _, ugettext
from solo.models import SingletonModel
from ckeditor.fields import CKEditorUploadField
from libs.storages import MediaStorage
from libs.color_field.fields import ColorField
from libs.stdimage.fields import StdImageField
from . import utils
from . import conf

re_newline_spaces = re.compile(r'[\r \t]*\n[\r \t]*')
re_newlines = re.compile(r'\n{3,}')
re_domain_urls = re.compile(r'(url\()(/[^/])')


class MailerConfig(SingletonModel):
    from_email = models.EmailField(_('sender email'), default='manager@example.com',
        help_text=_('should be real address')
    )
    from_name = models.CharField(_('sender name'), max_length=255, default='John Smith',
        help_text=_('should be real name')
    )

    bg_color = ColorField(_('background color'), blank=True, default='#BDC3C7')
    bg_image = models.ImageField(_('background image'), blank=True,
        storage=MediaStorage('mailerlite/campaigns')
    )

    preheader = models.TextField(_('pre-header'), blank=True)

    footer_text = models.TextField(_('text'), blank=True)
    website = models.CharField(_('website address'), max_length=255, default='example.com')
    contact_email = models.EmailField(_('contact email'), default='admin@example.com')

    import_groups_date = models.DateTimeField(default=now, editable=False)
    import_campaigns_date = models.DateTimeField(default=now, editable=False)
    import_subscribers_date = models.DateTimeField(default=now, editable=False)
    export_groups_date = models.DateTimeField(default=now, editable=False)
    export_campaigns_date = models.DateTimeField(default=now, editable=False)
    export_subscribers_date = models.DateTimeField(default=now, editable=False)

    class Meta:
        default_permissions = ('change',)
        verbose_name = _('settings')

    def __str__(self):
        return ugettext('Settings')


class Group(models.Model):
    STATUS_QUEUED = 0
    STATUS_PUBLISHED = 10
    STATUSES = (
        (STATUS_QUEUED, _('Queued')),
        (STATUS_PUBLISHED, _('Published')),
    )

    name = models.CharField(_('name'), max_length=255)
    total = models.PositiveIntegerField(_('total subscribers'), default=0, editable=False)
    active = models.PositiveIntegerField(_('active subscribers'), default=0, editable=False)
    unsubscribed = models.PositiveIntegerField(_('unsubscribed'), default=0, editable=False)
    status = models.SmallIntegerField(_('status'), choices=STATUSES, default=STATUS_QUEUED)

    sent = models.PositiveIntegerField(_('sent emails'), default=0, editable=False)
    opened = models.PositiveIntegerField(_('opened emails'), default=0, editable=False)
    clicked = models.PositiveIntegerField(_('clicks from emails'), default=0, editable=False)

    remote_id = models.PositiveIntegerField(_('ID in Mailerlite'), default=0, db_index=True, editable=False)
    date_created = models.DateTimeField(_('date created'), default=now, editable=False)
    date_updated = models.DateTimeField(_('date updated'), auto_now=True)

    class Meta:
        default_permissions = ('change',)
        verbose_name = _('list')
        verbose_name_plural = _('lists')
        ordering = ('-date_created',)

    def __str__(self):
        return self.name

    def update_from(self, json_data):
        self.remote_id = json_data['id']
        self.name = json_data['name']
        self.total = json_data['total'] or 0
        self.active = json_data['active'] or 0
        self.unsubscribed = json_data['unsubscribed'] or 0
        self.sent = json_data['sent'] or 0
        self.opened = json_data['opened'] or 0
        self.clicked = json_data['clicked'] or 0

        try:
            date_created = datetime.strptime(json_data['date_created'], '%Y-%m-%d %H:%M:%S')
        except (ValueError, TypeError):
            pass
        else:
            if date_created:
                self.date_created = date_created

        try:
            date_updated = datetime.strptime(json_data['date_updated'], '%Y-%m-%d %H:%M:%S')
        except (ValueError, TypeError):
            pass
        else:
            if date_updated:
                self.date_updated = date_updated


class Campaign(models.Model):
    STATUS_DRAFT = 0
    STATUS_QUEUED = 10
    STATUS_RUNNING = 20
    STATUS_DONE = 30
    STATUSES = (
        (STATUS_DRAFT, _('Draft')),
        (STATUS_QUEUED, _('Queued')),
        (STATUS_RUNNING, _('Running')),
        (STATUS_DONE, _('Done')),
    )

    groups = models.ManyToManyField(Group, verbose_name=_('lists'))
    subject = models.CharField(_('subject'), max_length=255)
    header_image = StdImageField(_('preview'),
        blank=True,
        storage=MediaStorage('mailerlite/campaigns'),
        min_dimensions=(640, 200),
        admin_variation='admin',
        crop_area=True,
        aspects='normal',
        variations=dict(
            normal=dict(
                size=(640, 200),
                quality=95,
            ),
            admin=dict(
                size=(480, 150),
            ),
        ),
    )
    text = CKEditorUploadField(_('text'), editor_options=conf.CKEDITOR_CONFIG)

    sent = models.PositiveIntegerField(_('sent emails'), default=0, editable=False)
    opened = models.PositiveIntegerField(_('opened emails'), default=0, editable=False)
    clicked = models.PositiveIntegerField(_('clicks from emails'), default=0, editable=False)

    status = models.SmallIntegerField(_('status'), choices=STATUSES, default=STATUS_DRAFT)
    published = models.BooleanField(_('published'), default=False)
    remote_id = models.PositiveIntegerField(_('ID in Mailerlite'), default=0, db_index=True, editable=False)
    remote_mail_id = models.PositiveIntegerField(_('ID in Mailerlite'), default=0, db_index=True, editable=False)
    date_created = models.DateTimeField(_('date created'), default=now, editable=False)
    date_started = models.DateTimeField(_('date started'), null=True, editable=False)
    date_done = models.DateTimeField(_('date done'), null=True, editable=False)

    class Meta:
        verbose_name = _('campaign')
        verbose_name_plural = _('campaigns')
        ordering = ('-date_created',)

    def __str__(self):
        return self.subject

    def get_absolute_url(self):
        return reverse('mailerlite:preview', kwargs={'campaign_id': self.pk})

    @property
    def subject_test(self):
        subject = self.subject.replace('{$name}', 'John')
        subject = subject.replace('{$last_name}', 'Smith')
        return subject

    def update_from(self, json_data, version=2):
        if version == 2:
            self.remote_id = json_data['id']
        else:
            self.remote_id = json_data['id']
            self.subject = json_data['subject']
            self.sent = json_data['total'] or 0
            self.opened = json_data['uniqueOpens'] or 0
            self.clicked = json_data['clicks'] or 0

            try:
                date_started = datetime.strptime(json_data['started'], '%Y-%m-%d %H:%M:%S')
            except (ValueError, TypeError):
                pass
            else:
                if date_started:
                    self.published = True
                    self.date_started = date_started
                    self.status = Campaign.STATUS_RUNNING

            try:
                date_done = datetime.strptime(json_data['started'], '%Y-%m-%d %H:%M:%S')
            except (ValueError, TypeError):
                pass
            else:
                if date_done:
                    self.published = True
                    self.date_done = date_done
                    self.status = Campaign.STATUS_DONE

    def render_html(self, request=None, scheme='//', test=False):
        content = loader.render_to_string('mailerlite/standart/html_version.html', {
            'config': MailerConfig.get_solo(),
            'campaign': self,
        }, request=request)
        content = content.replace('url(//', 'url(http://')
        content = utils.absolute_links(content, scheme=scheme)

        site = get_current_site(request)
        content = re_domain_urls.sub('\\1{}{}\\2'.format(scheme, site.domain), content)

        if test:
            content = content.replace('{$url}', '#')
            content = content.replace('{$unsubscribe}', '#')
            content = content.replace('{$email}', 'john@smithmail.com')
            content = content.replace('{$name}', 'John')
            content = content.replace('{$last_name}', 'Smith')
            content = content.replace('{$company}', 'Microsoft')

        return content

    def render_plain(self, request=None, test=False):
        content = loader.render_to_string('mailerlite/standart/plain_version.html', {
            'config': MailerConfig.get_solo(),
            'campaign': self,
        }, request=request)
        content = re_newline_spaces.sub('\n', content)
        content = re_newlines.sub('\n\n', content)

        if test:
            content = content.replace('{$url}', '#')
            content = content.replace('{$unsubscribe}', '#')
            content = content.replace('{$email}', 'john@smithmail.com')
            content = content.replace('{$name}', 'John')
            content = content.replace('{$last_name}', 'Smith')
            content = content.replace('{$company}', 'Microsoft')

        return content.strip()


class Subscriber(models.Model):
    STATUS_QUEUED = 0
    STATUS_SUBSCRIBED = 10
    STATUS_UNSUBSCRIBED = 20
    STATUSES = (
        (STATUS_QUEUED, _('Queued')),
        (STATUS_SUBSCRIBED, _('Subscribed')),
        (STATUS_UNSUBSCRIBED, _('Unsubscribed')),
    )

    groups = models.ManyToManyField(Group)
    email = models.EmailField(_('email'), unique=True)
    name = models.CharField(_('first name'), max_length=255, blank=True)
    last_name = models.CharField(_('last name'), max_length=255, blank=True)
    company = models.CharField(_('company'), max_length=255, blank=True)
    status = models.SmallIntegerField(_('status'), choices=STATUSES, default=STATUS_QUEUED)

    sent = models.PositiveIntegerField(_('sent emails'), default=0, editable=False)
    opened = models.PositiveIntegerField(_('opened emails'), default=0, editable=False)
    clicked = models.PositiveIntegerField(_('clicks from emails'), default=0, editable=False)

    remote_id = models.PositiveIntegerField(_('ID in Mailerlite'), default=0, db_index=True, editable=False)
    date_created = models.DateField(_('date subscribed'), default=now, editable=False)
    date_unsubscribe = models.DateTimeField(_('date unsubscribed'), null=True, editable=False)

    class Meta:
        default_permissions = ('add', 'change')
        verbose_name = _('subscriber')
        verbose_name_plural = _('subscribers')
        ordering = ('-date_created', )

    def __str__(self):
        return self.email

    def update_from(self, json_data):
        subscriber_fields = {
            field['key']: field['value']
            for field in json_data['fields']
        }

        self.remote_id = json_data['id']
        self.email = json_data['email']
        self.name = subscriber_fields['name'] or ''
        self.last_name = subscriber_fields['last_name'] or ''
        self.company = subscriber_fields['company'] or ''
        self.sent = json_data['sent'] or 0
        self.opened = json_data['opened'] or 0
        self.clicked = json_data['clicked'] or 0

        try:
            date_created = datetime.strptime(json_data['date_created'], '%Y-%m-%d')
        except (ValueError, TypeError):
            pass
        else:
            if date_created:
                self.date_created = date_created
                self.status = Subscriber.STATUS_SUBSCRIBED

        try:
            date_unsubscribe = datetime.strptime(json_data['date_unsubscribe'], '%Y-%m-%d %H:%M:%S')
        except (ValueError, TypeError):
            pass
        else:
            if date_unsubscribe:
                self.date_unsubscribe = date_unsubscribe
                self.status = Subscriber.STATUS_UNSUBSCRIBED
