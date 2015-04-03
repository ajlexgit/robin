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
                expression="title__icontains",
                minimum_input_length=0,
            )

"""

from .forms import AutocompleteField, AutocompleteMultipleField
