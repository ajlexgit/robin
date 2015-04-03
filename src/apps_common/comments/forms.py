import hashlib
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from libs.plainerror_form import PlainErrorFormMixin
from libs.protected_form import ProtectedModelFormMixin
from .models import Comment


class CommentForm(PlainErrorFormMixin, ProtectedModelFormMixin, forms.ModelForm):
    """ Форма добавления/редактирования комментария """
    hash = forms.CharField(
        widget = forms.HiddenInput,
        error_messages = {
            'invalid': 'Токен некорректен',
        }
    )
    
    protect_change_fields = ('content_type', 'object_id', 'parent')
    
    class Meta:
        model = Comment
        widgets = {
            'content_type': forms.HiddenInput(),
            'object_id': forms.HiddenInput(),
            'parent': forms.HiddenInput(),
            'text': forms.Textarea(attrs={
                'rows': 4,
            }),
        }
        error_messages = {
            'content_type': {
                'required': 'Тип сущности не указан',
                'invalid_choice': 'Тип сущности не найден',
            },
            'object_id': {
                'required': 'Cущность не указана',
            },
            'parent': {
                'invalid_choice': 'Родительский комментарий удален',
                'object_mismatch': 'Родительский комментарий находится на другой странице',
            },
            'text': {
                'required': 'Введите текст комментария',
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

    def clean_parent(self):
        parent = self.cleaned_data.get('parent')
        if parent is not None:
            content_type = self.cleaned_data.get('content_type')
            object_id = self.cleaned_data.get('object_id')
            if parent.content_type != content_type or parent.object_id != object_id:
                return self.add_field_error('parent', 'object_mismatch')
        return parent
        

class CommentValidationForm(PlainErrorFormMixin, forms.Form):
    """ Форма для валидации входных значений при действиях над комментом """
    content_type = forms.ModelChoiceField(
        queryset=ContentType.objects.all(),
        error_messages = {
            'required': 'Тип сущности не указан',
            'invalid_choice': 'Тип сущности не найден',
        }
    )
    object_id = forms.IntegerField(
        error_messages = {
            'required': 'Cущность не указана',
            'not_found': 'Cущность не найдена',
        }
    )
    comment = forms.ModelChoiceField(
        queryset=Comment.objects.all(),
        error_messages = {
            'required': 'Комментарий не указан',
            'invalid_choice': 'Комментарий удалён',
            'object_mismatch': 'Комментарий не относится к этой сущности',
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
        