from copy import deepcopy
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
                'from_name', 'from_email', 
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
        (_('Email footer'), {
            'fields': (
                'footer_text', 'website', 'contact_email',
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
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.published and not self.current_user.is_superuser:
            self.fields['header_image'].widget = ReadonlyFileWidget()
            self.fields['text'].widget.attrs['readonly'] = 'readonly'


@admin.register(Campaign)
class CampaignAdmin(ModelAdminMixin, admin.ModelAdmin):
    change_form_template = 'mailerlite/admin/change_form.html'

    fieldsets = (
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

    def get_fieldsets(self, request, obj=None):
        default = deepcopy(super().get_fieldsets(request, obj))
        if not obj:
            return default

        # Показываем группы, если их больше одной
        groups_count = Group.objects.count()
        if groups_count > 1:
            default = (
                (None, {
                    'fields': (
                        'groups',
                    )
                }),
            ) + default

        # Показ статистики
        if obj.published:
            default += (
                (_('Statistics'), {
                    'fields': (
                        'sent', 'opened', 'clicked', 'date_created', 'date_started', 'date_done',
                    )
                }),
            )

        # Доп инфа для суперадмина
        if request.user.is_superuser:
            default = (
                (_('Additional information'), {
                    'fields': (
                        'status', 'published', 'remote_id'
                    )
                }),
            ) + default
        return default

    def save_model(self, request, obj, form, change):
        """ Автоматически добавляем все группы, если они не заданы """
        super().save_model(request, obj, form, change)
        if not obj.groups.count() and Group.objects.count() <= 1:
            obj.groups.add(*Group.objects.all())

    def get_readonly_fields(self, request, obj=None):
        """ Если опубликован и не суперюзер - запрещаем редактирование """
        default = super().get_readonly_fields(request, obj)
        if obj and obj.published and not request.user.is_superuser:
            default += ('subject', 'groups',)
        return default

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj=obj, **kwargs)
        form.current_user = request.user
        return form

    def has_delete_permission(self, request, obj=None):
        """ Право на удаление суперюзеру """
        if request.user.is_superuser:
            return True
        return obj and obj.status == self.model.STATUS_DRAFT

    def get_actions(self, request):
        """ Массовое удаление только для суперюзера """
        default = super().get_actions(request)
        if not request.user.is_superuser and 'delete_selected' in default:
            del default['delete_selected']
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
                    {text}&nbsp;{action}
                </nobr>
            """.format(
                text=status_text,
                action=button_tpl.format(
                    href=reverse('admin:%s_%s_cancel' % info, args=(obj.id,)),
                    classes='btn-danger',
                    text=_('Cancel')
                ),
            )
        else:
            return status_text
    status_box.short_description = _('Status')
    status_box.admin_order_field = 'status'
    status_box.allow_tags = True

    def start_campaign(self, request, campaign_id):
        try:
            campaign = self.model.objects.get(pk=campaign_id, status=self.model.STATUS_DRAFT, published=False)
        except self.model.DoesNotExist:
            pass
        else:
            campaign.status = self.model.STATUS_QUEUED
            campaign.save()

        info = self.model._meta.app_label, self.model._meta.model_name
        return redirect('admin:%s_%s_changelist' % info)

    def cancel_campaign(self, request, campaign_id):
        try:
            campaign = self.model.objects.get(pk=campaign_id, status=self.model.STATUS_QUEUED, published=False)
        except self.model.DoesNotExist:
            pass
        else:
            campaign.remote_id = 0
            campaign.status = self.model.STATUS_DRAFT
            campaign.save()

        info = self.model._meta.app_label, self.model._meta.model_name
        return redirect('admin:%s_%s_changelist' % info)

    def sendtest(self, request, campaign_id):
        from premailer import Premailer
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
                'email',
            )
        }),
        (_('Additional information'), {
            'fields': (
                'name', 'last_name', 'company',
            )
        }),
    )
    readonly_fields = (
        'email', 'groups', 'status',
        'sent', 'opened', 'clicked', 'date_created', 'date_unsubscribe',
    )
    list_filter = ('status', )
    search_fields = ('email', 'name', 'last_name', 'company')
    list_display = ('email', 'sent', 'opened', 'clicked', 'status', 'date_created')

    def get_fieldsets(self, request, obj=None):
        default = deepcopy(super().get_fieldsets(request, obj))
        if obj is None:
            return default

        groups_count = Group.objects.count()
        if groups_count > 1:
            default[0][1]['fields'] += ('groups', )

        default[0][1]['fields'] += ('status',)

        default += (
            (_('Statistics'), {
                'fields': (
                    'sent', 'opened', 'clicked', 'date_created', 'date_unsubscribe'
                )
            }),
        )
        return default

    def get_readonly_fields(self, request, obj=None):
        default = list(super().get_readonly_fields(request, obj))
        if obj is None or obj.status == self.model.STATUS_QUEUED:
            for field in ('email', ):
                if field in default:
                    default.remove(field)
        if request.user.is_superuser:
            default.remove('status')
        return tuple(default)

    def save_model(self, request, obj, form, change):
        """ Автоматически добавляем все группы, если они не заданы """
        super().save_model(request, obj, form, change)
        if not obj.groups.count() and Group.objects.count() <= 1:
            obj.groups.add(*Group.objects.all())

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return obj and obj.status == self.model.STATUS_QUEUED

    def groups_list(self, obj):
        return ', '.join(group.name for group in obj.groups.all())
