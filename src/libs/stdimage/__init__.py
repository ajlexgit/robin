"""
    Зависит от:
        libs.variation_field

    Настройки:
        STDIMAGE_MAX_SIZE_DEFAULT = 12*1024*1024
        STDIMAGE_MIN_DIMENSIONS_DEFAULT = (0, 0)
        STDIMAGE_MAX_DIMENSIONS_DEFAULT = (6000, 6000)
        STDIMAGE_MAX_SOURCE_DIMENSIONS_DEFAULT = (2048, 2048)

    Пример:
        preview = StdImageField(_('preview'),
            blank=True,
            storage=MediaStorage('main/header'),
            admin_variation='square',
            crop_area=True,
            crop_field='preview_crop',
            aspects=('normal', ),
            variations=dict(
                normal=dict(
                    size=(800, 600),
                ),
                square=dict(
                    size=(280, 280),
                    mask='module/img/square_mask.png',
                    overlay='module/img/square_overlay.png',
                ),
            ),
        )
        preview_crop = models.CharField(_('stored_crop'),
            max_length=32,
            blank=True,
            editable=False,
        )

"""

from .fields import StdImageField
from .widgets import StdImageWidget, StdImageAdminWidget

__all__ = ['StdImageField']