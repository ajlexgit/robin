from django import forms
from django.contrib import admin
from django.conf.urls import url
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from solo.admin import SingletonModelAdmin
from project.admin import ModelAdminMixin
from libs.description import description
from libs.widgets import ReadonlyFileWidget
from libs.autocomplete.widgets import AutocompleteMultipleWidget
from .models import MailerConfig, Group, Campaign, Subscriber


@admin.register(MailerConfig)
class MailerConfigAdmin(ModelAdminMixin, SingletonModelAdmin):
    fieldsets = (
        (_('Email sender'), {
            'fields': (
                'from_email', 'from_name',
            ),
        }),
        (_('Email style'), {
            'fields': (
                'bg_color', 'bg_image',
            ),
        }),
        (_('Email footer'), {
            'fields': (
                'company', 'website', 'contact_email',
            ),
        }),
    )


@admin.register(Group)
class GroupAdmin(ModelAdminMixin, admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'name', 'status',
            )
        }),
        (_('Subscribers'), {
            'fields': (
                'total', 'active', 'unsubscribed',
            )
        }),
        (_('Statistics'), {
            'fields': (
                'sent', 'opened', 'clicked', 'date_created', 'date_updated',
            )
        }),
    )
    readonly_fields = (
        'status', 'total', 'active', 'unsubscribed', 'sent', 'opened', 'clicked', 'date_created', 'date_updated'
    )
    list_display = ('name', 'total', 'active', 'unsubscribed', 'sent', 'opened', 'clicked', 'status')


class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = '__all__'
        widgets = {
            'groups': AutocompleteMultipleWidget(
                expressions='name__icontains',
                minimum_input_length=0,
            ),
            'from_name': forms.TextInput(
                attrs={
                    'class': 'input-xlarge',
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and not self.instance.editable:
            self.fields['header_image'].widget = ReadonlyFileWidget()
            self.fields['text'].widget.attrs['readonly'] = 'readonly'


@admin.register(Campaign)
class CampaignAdmin(ModelAdminMixin, admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'groups', 'status',
            )
        }),
        (_('Content'), {
            'fields': (
                'subject', 'preheader', 'header_image', 'text',
            )
        }),
        (_('Statistics'), {
            'fields': (
                'sent', 'opened', 'clicked', 'date_created', 'date_started', 'date_done',
            )
        }),
    )
    form = CampaignForm
    readonly_fields = (
        'status', 'sent', 'opened', 'clicked', 'date_created', 'date_started', 'date_done'
    )
    actions = ('action_start', )
    list_filter = ('status', )
    list_display = ('view', 'short_subject', 'sent', 'opened', 'clicked', 'status_box')
    list_display_links = ('short_subject', )

    def get_readonly_fields(self, request, obj=None):
        default = self.readonly_fields
        if obj and not obj.editable:
            default += ('groups', 'subject', 'preheader')
        return default

    def short_subject(self, obj):
        return description(obj.subject, 30, 60)
    short_subject.short_description = _('Subject')
    short_subject.admin_order_field = 'subject'

    def status_box(self, obj):
        status_text = dict(self.model.STATUSES).get(obj.status)
        if obj.status == self.model.STATUS_DRAFT:
            info = self.model._meta.app_label, self.model._meta.model_name
            start_url = reverse('admin:%s_%s_start' % info, args=(obj.id, ))
            button = '<a href="%s" class="btn btn-mini btn-success" style="margin-left: 10px">Start</a>' % start_url
            return '%s %s' % (status_text, button)
        elif obj.status == self.model.STATUS_QUEUED:
            info = self.model._meta.app_label, self.model._meta.model_name
            cancel_url = reverse('admin:%s_%s_cancel' % info, args=(obj.id,))
            button = '<a href="%s" class="btn btn-mini btn-danger" style="margin-left: 10px">Cancel</a>' % cancel_url
            return '%s %s' % (status_text, button)
        else:
            return status_text
    status_box.short_description = _('Status')
    status_box.admin_order_field = 'status'
    status_box.allow_tags = True

    def get_urls(self):
        urls = super().get_urls()
        info = self.model._meta.app_label, self.model._meta.model_name
        submit_urls = [
            url(r'^(\d+)/start/$', self.admin_site.admin_view(self.start_campaign), name='%s_%s_start' % info),
            url(r'^(\d+)/cancel/$', self.admin_site.admin_view(self.cancel_campaign), name='%s_%s_cancel' % info),
        ]
        return submit_urls + urls

    def action_start(self, request, queryset):
        queryset.filter(status=self.model.STATUS_DRAFT).update(status=self.model.STATUS_QUEUED)
    action_start.short_description = _('Start campaign')

    def start_campaign(self, request, campaign_id):
        try:
            campaign = self.model.objects.get(pk=campaign_id, status=self.model.STATUS_DRAFT)
        except self.model.DoesNotExist:
            pass
        else:
            campaign.status = self.model.STATUS_QUEUED
            campaign.save()

        info = self.model._meta.app_label, self.model._meta.model_name
        return redirect('admin:%s_%s_changelist' % info)

    def cancel_campaign(self, request, campaign_id):
        try:
            campaign = self.model.objects.get(pk=campaign_id, status=self.model.STATUS_QUEUED)
        except self.model.DoesNotExist:
            pass
        else:
            campaign.remote_id = 0
            campaign.status = self.model.STATUS_DRAFT
            campaign.save()

        info = self.model._meta.app_label, self.model._meta.model_name
        return redirect('admin:%s_%s_changelist' % info)


@admin.register(Subscriber)
class SubscriberAdmin(ModelAdminMixin, admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'groups', 'email', 'status',
            )
        }),
        (_('Addition information'), {
            'fields': (
                'name', 'last_name', 'company',
            )
        }),
        (_('Statistics'), {
            'fields': (
                'sent', 'opened', 'clicked', 'date_created', 'date_unsubscribe'
            )
        }),
    )
    readonly_fields = (
        'groups', 'email', 'status', 'name', 'last_name', 'company',
        'sent', 'opened', 'clicked', 'date_created', 'date_unsubscribe',
    )
    list_filter = ('status', )
    search_fields = ('email', 'name', 'last_name', 'company')
    list_display = ('email', 'groups_list', 'sent', 'opened', 'clicked', 'status')

    def groups_list(self, obj):
        return ', '.join(group.name for group in obj.groups.all())
