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
        # page/models.py:
            class SubType(models.Model):
                ...

                @staticmethod
                def autocomplete_item(obj):
                    # Свой формат пунктов списка
                    text = '–' * obj.level + obj.title
                    return {
                        'id': obj.pk,
                        'text': '<span style="color: red;">%s</span>' % text,
                        'selected_text': '<span style="color: green;">%s</span>' % text,
                    }

        # page/admin.py:
            class PostAdminForm(forms.ModelForm):

                class Meta:
                    widgets = {
                        'post_subtype': AutocompleteWidget(
                            dependencies = (
                                ('sections', 'sections', True),
                            ),
                            attrs = {
                                'style': 'width:50%',
                            },
                            minimum_input_length = 0,
                            format_item = SubType.autocomplete_item,
                        )
                    }


    Пример текстового поля с автокомплитом:
        # page/admin.py:
            def get_object_choices():
                return ('Pencil', 'Pen', 'Table', 'Chair')

            class PostAdminForm(forms.ModelForm):

                class Meta:
                    widgets = {
                        'producer': AutocompleteTextboxWidget(
                            choices=get_object_choices,
                            attrs={
                                'style': 'width:50%',
                            }
                        )
                    }

"""

from .widgets import AutocompleteWidget, AutocompleteMultipleWidget, AutocompleteTextboxWidget

__all__ = ['AutocompleteWidget', 'AutocompleteMultipleWidget', 'AutocompleteTextboxWidget']