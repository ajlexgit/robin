from django import forms
from django.contrib import admin
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
                'name',
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
        'total', 'active', 'unsubscribed', 'sent', 'opened', 'clicked', 'date_created', 'date_updated'
    )
    list_display = ('name', 'total', 'active', 'unsubscribed', 'sent', 'opened', 'clicked')

    # def has_add_permission(self, request):
    #     return False

    # def has_delete_permission(self, request, obj=None):
    #     return False


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
    list_display = ('view', 'short_subject', 'status', 'sent', 'opened', 'clicked')
    list_display_links = ('short_subject', )

    def get_readonly_fields(self, request, obj=None):
        default = self.readonly_fields
        if obj and not obj.editable:
            default += ('subject',)
        return default

    def short_subject(self, obj):
        return description(obj.subject, 30, 60)
    short_subject.short_description = _('Subject')
    short_subject.admin_order_field = 'subject'

    def action_start(self, request, queryset):
        queryset.filter(status=Campaign.STATUS_DRAFT).update(status=Campaign.STATUS_QUEUED)
    action_start.short_description = _('Start campaign')


@admin.register(Subscriber)
class SubscriberAdmin(ModelAdminMixin, admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'groups', 'email',
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
        'groups', 'email', 'name', 'last_name', 'company',
        'sent', 'opened', 'clicked', 'date_created', 'date_unsubscribe',
    )
    search_fields = ('email', 'name', 'last_name', 'company')
    list_display = ('email', 'groups_list', 'sent', 'opened', 'clicked', 'date_created')

    def groups_list(self, obj):
        return ', '.join(group.name for group in obj.groups.all())
