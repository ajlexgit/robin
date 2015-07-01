from django.db import models
from django.core import exceptions
from django.contrib.staticfiles.storage import staticfiles_storage
from libs.checks import FieldChecksMixin
from .forms import SpriteImageFormField
from .widgets import SpriteImageWidget


class Icon:
    def __init__(self, url='', name='', position=()):
        self.url = url
        self._name = name
        self._position = position

    def __getitem__(self, item):
        return self._position[item]

    def __bool__(self):
        return bool(self._name and self._position)

    def __str__(self):
        return self._name


class SpriteImageDescriptor:
    def __init__(self, field):
        self.field = field

    def __get__(self, instance=None, owner=None):
        if instance is None:
            raise AttributeError(
                "The '%s' attribute can only be accessed from %s instances."
                % (self.field.name, owner.__name__))

        value = instance.__dict__[self.field.name]

        key = str(value)
        choices_dict = dict(self.field.choices)
        icon = self.field.attr_class(self.field.sprite_url, key, choices_dict.get(key, ()))
        instance.__dict__[self.field.name] = icon

        return instance.__dict__[self.field.name]

    def __set__(self, instance, value):
        instance.__dict__[self.field.name] = value


class SpriteImageField(FieldChecksMixin, models.CharField):
    descriptor_class = SpriteImageDescriptor
    attr_class = Icon

    def __init__(self, *args, sprite='', size=(), **kwargs):
        kwargs.setdefault('max_length', 100)
        super().__init__(*args, **kwargs)
        self.sprite = sprite
        self.sprite_url = staticfiles_storage.url(self.sprite)
        self.size = size

    def custom_check(self):
        errors = []

        if not self.sprite:
            errors.append(
                self.check_error('sprite required')
            )
        else:
            if not staticfiles_storage.exists(self.sprite):
                errors.append(
                    self.check_error('sprite %s not found' % self.sprite)
                )

        if not self.size:
            errors.append(
                self.check_error('size required')
            )
        elif not isinstance(self.size, (list, tuple)) or len(self.size) != 2:
            errors.append(
                self.check_error('size should be a two-element list or tuple')
            )

        return errors

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs['sprite'] = self.sprite
        kwargs['size'] = self.size
        if kwargs['max_length'] == 100:
            del kwargs['max_length']
        return name, path, args, kwargs

    def contribute_to_class(self, cls, *args, **kwargs):
        super().contribute_to_class(cls, *args, **kwargs)
        setattr(cls, self.name, self.descriptor_class(self))

    def validate(self, value, model_instance):
        """
        Validates value and throws ValidationError. Subclasses should override
        this to provide validation logic.
        """
        if not self.editable:
            # Skip validation for non-editable fields.
            return

        if self._choices and value not in self.empty_values:
            for option_key, option_value in self.choices:
                if value == option_key:
                    return
            raise exceptions.ValidationError(
                self.error_messages['invalid_choice'],
                code='invalid_choice',
                params={'value': value},
            )

        if value is None and not self.null:
            raise exceptions.ValidationError(self.error_messages['null'], code='null')

        if not self.blank and value in self.empty_values:
            raise exceptions.ValidationError(self.error_messages['blank'], code='blank')

    def formfield(self, **kwargs):
        kwargs.update({
            'choices_form_class': SpriteImageFormField,
            'widget': SpriteImageWidget(
                sprite=self.sprite_url,
                size=self.size,
            ),
        })
        return super().formfield(**kwargs)