from .fields import StdImageField, ACTION_CROP, ACTION_CROP_ANYWAY, ACTION_STRETCH_BY_WIDTH, ACTION_INSCRIBE


"""
    Настройки:
        STDIMAGE_MAX_SIZE_DEFAULT = 12*1024*1024
        STDIMAGE_MIN_DIMENSIONS_DEFAULT = (0, 0)
        STDIMAGE_MAX_DIMENSIONS_DEFAULT = (6000, 6000)
        STDIMAGE_MAX_SOURCE_DIMENSIONS_DEFAULT = (2048, 2048)
    
    Пример:
        PREVIEW_PATH = 'preview'
        PREVIEW_NORMAL = (800, 600)
        PREVIEW_SQUARE = (280, 280)
        
        preview = StdImageField('превью',
            upload_to=PREVIEW_PATH,
            blank=True,
            admin_variation='square',
            min_dimensions=(100, 100),
            max_dimensions=(6000, 6000),
            max_source_dimensions=(2048, 2048),
            max_size=20*1024*1024,
            crop_area=True,
            aspects=('normal', 'square', 1.5),
            variations=dict(
                normal=dict(
                    size=PREVIEW_NORMAL,
                ),
                square=dict(
                    size=PREVIEW_SQUARE,
                    mask='posts/img/square_mask.png',
                    overlay='posts/img/square_overlay.png',
                ),
            ),
        )

"""