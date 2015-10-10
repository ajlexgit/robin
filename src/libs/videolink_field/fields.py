from django.core.exceptions import ValidationError
from django.db import models
from django.core import checks
from libs.widgets import URLWidget
from .videolink import VideoLink
from .formfields import VideoLinkFormField
from .providers import PROVIDERS


class VideoLinkField(models.Field, metaclass=models.SubfieldBase):
    def __init__(self, *args, providers=set(), **kwargs):
        kwargs['max_length'] = 64
        self._providers = set(providers)
        super().__init__(*args, **kwargs)

    def get_internal_type(self):
        return "CharField"

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs['max_length']
        kwargs['providers'] = self._providers
        return name, path, args, kwargs

    def check(self, **kwargs):
        errors = super().check(**kwargs)
        errors.extend(self._check_providers(**kwargs))
        return errors

    def _check_providers(self, **kwargs):
        if not self._providers:
            return []

        if not isinstance(self._providers, (set, list, tuple)):
            return [
                checks.Error(
                    'providers must be set, list or tuple',
                    obj=self
                )
            ]

        errors = []
        for provider in self._providers:
            if provider not in PROVIDERS:
                errors.append(
                    checks.Error(
                        'provider unknown: %s' % provider,
                        obj=self
                    )
                )
        return errors

    def from_db_value(self, value, *args, **kwargs):
        if not value:
            return None
        elif isinstance(value, str):
            return VideoLink(value, self._providers)
        else:
            raise ValueError('Invalid video type: %r' % value)

    def get_prep_value(self, value):
        if not value:
            return ''
        elif isinstance(value, VideoLink):
            return repr(value)
        else:
            raise TypeError('Invalid video type: %r' % value)

    def to_python(self, value):
        if not value:
            return None
        elif isinstance(value, VideoLink):
            return value
        elif isinstance(value, str):
            try:
                return VideoLink(value, self._providers)
            except (TypeError, ValueError) as e:
                raise ValidationError(e)
        else:
            raise ValidationError('Invalid video type: %r' % value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_prep_value(value)

    def formfield(self, **kwargs):
        kwargs.update({
            'form_class': VideoLinkFormField,
            'providers': self._providers,
            'widget': URLWidget(attrs={
                'class': 'input-xxlarge',
            }),
        })
        return super().formfield(**kwargs)
