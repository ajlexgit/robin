from copy import deepcopy
from premailer import Premailer
from django import forms
from django.conf import settings
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


class MailerConfigForm(forms.ModelForm):
    class Meta:
        model = MailerConfig
        fields = '__all__'
        widgets = {
            'from_name': forms.TextInput(
                attrs={
                    'class': 'input-xlarge',
                }
            ),
            'company': forms.TextInput(
                attrs={
                    'class': 'input-xlarge',
                }
            ),
            'website': forms.TextInput(
                attrs={
                    'class': 'input-xlarge',
                }
            ),
        }


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
        (_('Email header'), {
            'fields': (
                'preheader',
            ),
        }),
        (_('Contact us'), {
            'fields': (
                'contact_text',
            ),
        }),
        (_('Email footer'), {
            'fields': (
                'footer_text', 'facebook', 'website', 'contact_email',
            ),
        }),
    )
    form = MailerConfigForm


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
        'total', 'active', 'unsubscribed', 'sent', 'opened', 'clicked', 'date_created', 'date_updated'
    )
    list_display = ('name', 'total', 'active', 'unsubscribed', 'sent', 'opened', 'clicked', 'status')

    def get_readonly_fields(self, request, obj=None):
        default = super().get_readonly_fields(request, obj)
        if not request.user.is_superuser:
            default += ('status', )
        return default

    def has_add_permission(self, request):
        """ Право на добавление суперюзеру """
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        """ Право на удаление суперюзеру """
        default = super().has_delete_permission(request, obj)
        is_draft = obj and obj.status == self.model.STATUS_QUEUED
        if request.user.is_superuser:
            return True
        else:
            return default and is_draft


class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = '__all__'
        widgets = {
            'groups': AutocompleteMultipleWidget(
                expressions='name__icontains',
                minimum_input_length=0,
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.published:
            self.fields['header_image'].widget = ReadonlyFileWidget()
            self.fields['text'].widget.attrs['readonly'] = 'readonly'


@admin.register(Campaign)
class CampaignAdmin(ModelAdminMixin, admin.ModelAdmin):
    change_form_template = 'mailerlite/admin/change_form.html'

    fieldsets = (
        (None, {
            'fields': (
                'groups',
            )
        }),
        (_('Content'), {
            'fields': (
                'subject', 'header_image', 'text',
            )
        }),
    )
    form = CampaignForm
    readonly_fields = (
        'sent', 'opened', 'clicked', 'date_created', 'date_started', 'date_done', 'remote_id'
    )
    actions = ('action_start', )
    list_filter = ('status', )
    list_display = ('view', 'short_subject', 'sent', 'opened', 'clicked', 'status_box', 'date_created')
    list_display_links = ('short_subject', )

    class Media:
        js = (
            'mailerlite/admin/js/sendtest.js',
        )
        css = {
            'all': (
                'mailerlite/admin/css/sendtest.css',
            )
        }

    def get_readonly_fields(self, request, obj=None):
        default = super().get_readonly_fields(request, obj)
        if obj and obj.published:
            default += ('subject',)
            if not request.user.is_superuser:
                default += ('groups',)
        return default

    def has_delete_permission(self, request, obj=None):
        """ Право на удаление суперюзеру """
        default = super().has_delete_permission(request, obj)
        is_draft = obj and obj.status in (self.model.STATUS_DRAFT, self.model.STATUS_QUEUED)
        if request.user.is_superuser:
            return True
        else:
            return default and is_draft

    def get_actions(self, request):
        default = super().get_actions(request)
        if not request.user.is_superuser and 'delete_selected' in default:
            del default['delete_selected']
        return default

    def get_fieldsets(self, request, obj=None):
        default = deepcopy(super().get_fieldsets(request, obj))
        if obj and request.user.is_superuser:
            default[0][1]['fields'] += ('status', 'published', 'remote_id')
            if obj.published:
                default += (
                    (_('Statistics'), {
                        'fields': (
                            'sent', 'opened', 'clicked', 'date_created', 'date_started', 'date_done',
                        )
                    }),
                )
        return default

    def get_changeform_initial_data(self, request):
        return {
            'groups': Group.objects.values_list('pk', flat=True),
        }

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        if not add:
            info = self.model._meta.app_label, self.model._meta.model_name
            context.update({
                'sendtest_url': reverse('admin:%s_%s_sendtest' % info, args=(obj.pk,)),
            })
        return super().render_change_form(request, context, add, change, form_url, obj)

    def get_urls(self):
        urls = super().get_urls()
        info = self.model._meta.app_label, self.model._meta.model_name
        submit_urls = [
            url(r'^(\d+)/start/$', self.admin_site.admin_view(self.start_campaign), name='%s_%s_start' % info),
            url(r'^(\d+)/cancel/$', self.admin_site.admin_view(self.cancel_campaign), name='%s_%s_cancel' % info),
            url(r'^(\d+)/sendtest/$', self.admin_site.admin_view(self.sendtest), name='%s_%s_sendtest' % info),
        ]
        return submit_urls + urls

    def short_subject(self, obj):
        return description(obj.subject, 30, 60)
    short_subject.short_description = _('Subject')
    short_subject.admin_order_field = 'subject'

    def status_box(self, obj):
        status_text = dict(self.model.STATUSES).get(obj.status)
        info = self.model._meta.app_label, self.model._meta.model_name
        button_tpl = '<a href="{href}" class="btn btn-mini {classes}" style="margin-left: 5px">{text}</a>'

        if obj.status == self.model.STATUS_DRAFT:
            return """
                <nobr>
                    {text}&nbsp;{action}&nbsp;{delete}
                </nobr>
            """.format(
                text=status_text,
                action=button_tpl.format(
                    href=reverse('admin:%s_%s_start' % info, args=(obj.id,)),
                    classes='btn-success',
                    text=_('Start')
                ),
                delete=button_tpl.format(
                    href=reverse('admin:%s_%s_delete' % info, args=(obj.id,)),
                    classes='btn-danger',
                    text=_('Delete')
                ),
            )
        elif obj.status == self.model.STATUS_QUEUED and not obj.published:
            return """
                <nobr>
                    {text}&nbsp;{action}&nbsp;{delete}
                </nobr>
            """.format(
                text=status_text,
                action=button_tpl.format(
                    href=reverse('admin:%s_%s_cancel' % info, args=(obj.id,)),
                    classes='btn-danger',
                    text=_('Cancel')
                ),
                delete=button_tpl.format(
                    href=reverse('admin:%s_%s_delete' % info, args=(obj.id,)),
                    classes='btn-danger',
                    text=_('Delete')
                ),
            )
        else:
            return status_text
    status_box.short_description = _('Status')
    status_box.admin_order_field = 'status'
    status_box.allow_tags = True

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

    def sendtest(self, request, campaign_id):
        from django.http import JsonResponse, Http404
        from django.core.mail import send_mail, BadHeaderError

        receiver = request.POST.get('receiver')
        if not receiver:
            raise Http404

        try:
            campaign = self.model.objects.get(pk=campaign_id)
        except self.model.DoesNotExist:
            pass
        else:
            content = campaign.render_html(request, scheme='http://', test=True)
            content = Premailer(content, strip_important=False).transform()
            plain = campaign.render_plain(request, test=True)

            try:
                send_mail(
                    campaign.subject, plain, settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[receiver],
                    html_message=content
                )
            except BadHeaderError:
                pass

        return JsonResponse({})


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
    )
    readonly_fields = (
        'groups', 'name', 'last_name', 'company',
        'sent', 'opened', 'clicked', 'date_created', 'date_unsubscribe',
    )
    list_filter = ('status', )
    search_fields = ('email', 'name', 'last_name', 'company')
    list_display = ('email', 'sent', 'opened', 'clicked', 'status', 'date_created')

    def get_readonly_fields(self, request, obj=None):
        default = super().get_readonly_fields(request, obj)
        if not request.user.is_superuser:
            default += ('status', 'email')
        return default

    def get_fieldsets(self, request, obj=None):
        default = super().get_fieldsets(request, obj)
        if request.user.is_superuser:
            default += (
                (_('Statistics'), {
                    'fields': (
                        'sent', 'opened', 'clicked', 'date_created', 'date_unsubscribe'
                    )
                }),
            )
        return default

    def groups_list(self, obj):
        return ', '.join(group.name for group in obj.groups.all())
