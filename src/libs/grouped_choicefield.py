from itertools import groupby
from django import forms
from django.utils.encoding import smart_text


class GroupedModelChoiceField(forms.ModelChoiceField):
    """
        Поле формы, группирующее (<optgroup>) список сущностей
        по значению одного из полей этих сущностей.

        Пример:
            # models.py:
                class Category(models.Model):
                    ...

                class Product(models.Model):
                    category = models.ForeignKey(Category)
                    ...

                class ProductProperty(models.Model):
                    product = models.ForeignKey(Product)

            # admin.py:
                class ProductPropertyForm(forms.ModelForm):
                    parent = GroupedModelChoiceField(
                        queryset=Product.objects.all(),
                        group_by='category',
                    )

                    class Meta:
                        model = ProductProperty
                        fields = '__all__'
    """
    def __init__(self, *args, group_by=None, group_label=None, **kwargs):
        self.group_by = group_by
        self.group_label = group_label or smart_text
        super().__init__(*args, **kwargs)

    def _get_choices(self):
        if hasattr(self, '_choices'):
            return self._choices
        return GroupedModelChoiceIterator(self)

    choices = property(_get_choices, forms.ModelChoiceField._set_choices)


class GroupedModelChoiceIterator(forms.models.ModelChoiceIterator):
    def __iter__(self):
        if self.field.group_by is None:
            yield from super().__iter__()
            return

        if self.field.empty_label is not None:
            yield ("", self.field.empty_label)

        groups = groupby(
            self.queryset.all(),
            key=lambda row: getattr(row, self.field.group_by)
        )
        for group, choices in groups:
            yield self.field.group_label(group), [self.choice(ch) for ch in choices]
