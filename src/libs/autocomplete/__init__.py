"""
    Установка:
        settings.py:
            INSTALLED_APPS = (
                ...
                'libs.autocomplete',
                ...
            )

        urls.py:
            ...
            url(r'^autocomplete/', include('libs.autocomplete.urls', namespace='autocomplete')),
            ...

    Необязательные настройки:
        AUTOCOMPLETE_CACHE_BACKEND = 'default'

    Пример:
        class PostAdminForm(forms.ModelForm):
            post_subtype = AutocompleteField(
                queryset=Post.objects.all(),
                dependencies=(
                    ('sections', 'sections', True),
                ),
                expressions="title__icontains",
                minimum_input_length=0,
            )

    Пример кастомизации выводимых пунктов:
        models.py:
            class ShopCategory(models.Model):
                ...

                @staticmethod
                def autocomplete_item(obj):
                    text = '–' * obj.level + obj.title
                    return {
                        'id': obj.pk,
                        'text': '<span style="color: red;">%s</span>' % text,
                        'selected_text': '<span style="color: green;">%s</span>' % text,
                    }

        admin.py:
            class ProductAdminForm(forms.ModelForm):
                category = AutocompleteField(
                    queryset = ShopCategory.objects.all(),
                    expressions = "title__icontains",
                    item2dict_func = ShopCategory.autocomplete_item,
                )

"""

from .forms import AutocompleteField, AutocompleteMultipleField

__all__ = ['AutocompleteField', 'AutocompleteMultipleField']