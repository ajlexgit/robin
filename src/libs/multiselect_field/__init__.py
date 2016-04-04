"""
    Поле, которое может принимать набор значений из фиксированного списка
    choices. Значения в БД разделяются запятыми.

    Пример:
        class SomeModel(models.Model):
            LANGUAGES = (
                (1, _('English')),
                (2, _('Russian')),
                (3, _('Japanese')),
                (4, _('Italian')),
            )

            langs = MultiSelectField(_('langs'), choices=LANGUAGES, blank=True)

    Пример значения в модели:
        >>> instance.langs
        >>> (1, 3)

        >>> instance_empty.langs
        >>> ()

"""
from .fields import MultiSelectField
from .forms import MultiSelectFormField
