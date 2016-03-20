import hashlib
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from form_helper import FormHelperMixin
from .models import Comment


class CommentForm(FormHelperMixin, forms.ModelForm):
    """ Форма добавления/редактирования комментария """
    hash = forms.CharField(
        widget = forms.HiddenInput,
        error_messages = {
            'invalid': 'Invalid token',
        }
    )

    class Meta:
        model = Comment
        fields = '__all__'
        widgets = {
            'content_type': forms.HiddenInput(),
            'object_id': forms.HiddenInput(),
            'parent': forms.HiddenInput(),
            'text': forms.Textarea(attrs={
                'rows': 4,
                'autofocus': True,
            }),
        }
        error_messages = {
            'content_type': {
                'required': 'content_type is required',
                'invalid_choice': 'invalid content_type',
            },
            'object_id': {
                'required': 'object_id is required',
            },
            'parent': {
                'invalid_choice': 'parent comment was deleted',
                'object_mismatch': 'parent comment attached to another objetc',
            },
            'text': {
                'required': 'text is required',
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['hash'].initial = self.build_hash()

    def build_hash(self):
        content_type = self['content_type'].value()
        object_id = self['object_id'].value()
        hashkey = 'ct:{}:oi:{}'.format(content_type, object_id)
        return hashlib.md5(hashkey.encode()).hexdigest()

    def clean_hash(self):
        form_hash = self.cleaned_data.get('hash')
        true_hash = self.build_hash()
        if form_hash != true_hash:
            return self.add_field_error('hash', 'invalid')
        return form_hash

    def clean_content_type(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.content_type
        else:
            return self.cleaned_data['content_type']

    def clean_object_id(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.object_id
        else:
            return self.cleaned_data['object_id']

    def clean_parent(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            parent = instance.parent
        else:
            parent = self.cleaned_data['parent']

        if parent is not None:
            content_type = self.cleaned_data.get('content_type')
            object_id = self.cleaned_data.get('object_id')
            if parent.content_type != content_type or parent.object_id != object_id:
                return self.add_field_error('parent', 'object_mismatch')
        return parent


class CommentValidationForm(FormHelperMixin, forms.Form):
    """ Форма для валидации входных значений при действиях над комментом """
    content_type = forms.ModelChoiceField(
        queryset=ContentType.objects.all(),
        error_messages = {
            'required': 'content_type is required',
            'invalid_choice': 'invalid content_type',
        }
    )
    object_id = forms.IntegerField(
        error_messages = {
            'required': 'object_id is required',
            'not_found': 'object not found',
        }
    )
    comment = forms.ModelChoiceField(
        queryset=Comment.objects.all(),
        error_messages = {
            'required': 'comment is required',
            'invalid_choice': 'comment was deleted',
            'object_mismatch': 'comment attached to another object',
        }
    )

    def clean_object_id(self):
        content_type = self.cleaned_data.get('content_type')
        object_id = self.cleaned_data.get('object_id')
        try:
            obj = content_type.get_object_for_this_type(pk=object_id)
        except ObjectDoesNotExist:
            return self.add_field_error('object_id', 'not_found')
        return obj

    def clean(self):
        obj = self.cleaned_data.get('object_id')
        comment = self.cleaned_data.get('comment')
        if obj and comment and comment.entity != obj:
            return self.add_field_error('comment', 'object_mismatch')

