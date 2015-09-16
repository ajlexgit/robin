"""
    Поле для выбора иконки из спрайта.

    Зависит от:
        libs.checks

    Пример:
        models.py:
            class MyModel(models.Model):
                ICONS = (
                    ('no_defence', (-230, 0)),
                    ('area', (-260, 0)),
                    ('touch', (-290, 0)),
                    ('leaf', (-320, 0)),
                    ('shield', (-350, 0)),
                    ('dots', (-380, 0)),
                    ('no_bacterial', (-410, 0)),
                )

                ...

                icon = SpriteImageField(_('icon'),
                    sprite='img/sprite.svg',
                    size=(30, 30),
                    choices=ICONS,
                    default=ICONS[0][0],
                )

        template.html:
            # Вывод имени ключа
            <div class="{{ object.icon }}">

            # Вывод координат
            <div style="background-position: {{ object.icon.0 }}px {{ object.icon.1 }}px">

            # Вывод ссылки на картинку
            <div style="background-image: {{ object.icon.url }}">

"""

from .fields import SpriteImageField

__all__ = ['SpriteImageField']