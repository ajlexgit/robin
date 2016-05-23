from collections import namedtuple

# ===============================
#   Наборы скриптов с зависимостями.
#
#   Пример использования:
#       'some_page': {
#           'source_filenames': PopupGallery.css + (
#           ...
#           ),
#           ...
#       }
# ===============================

# Слайдер
Slider = namedtuple('Slider', ['css', 'js'])(
    css=(
        'scss/slider/slider.scss',
        'scss/slider/plugins/controls.scss',
        'scss/slider/plugins/navigation.scss',
    ),
    js=(
        'js/drager.js',
        'js/slider/slider.js',
        'js/slider/win_height_slider.js',
        'js/slider/plugins/side_animation.js',
        'js/slider/plugins/fade_animation.js',
        'js/slider/plugins/autoscroll.js',
        'js/slider/plugins/navigation.js',
        'js/slider/plugins/controls.js',
        'js/slider/plugins/drag.js',
    )
)

# Галерея во всплывающем окне
PopupGallery = namedtuple('PopupGallery', ['css', 'js'])(
    css=Slider.css + (
        'gallery/scss/gallery_popup.scss',
    ),
    js=(
        'js/jquery.youtube.js',
        'js/jquery.vimeo.js',
    ) + Slider.js + (
        'gallery/js/gallery_popup.js',
    )
)

# ===============================
#   Скрипты
# ===============================

PIPELINE = {
    'PIPELINE_ENABLED': True,
    'COMPILERS': (
        'libs.pipeline.sassc.SASSCCompiler',
    ),
    'SASS_ARGUMENTS': '-t compressed',
    'CSS_COMPRESSOR': 'libs.pipeline.cssmin.CSSCompressor',
    'JS_COMPRESSOR': 'pipeline.compressors.jsmin.JSMinCompressor',

    'STYLESHEETS': {
        'core': {
            'source_filenames': (
                'scss/grid.scss',
                'scss/layout.scss',
                'scss/forms.scss',
                'scss/buttons.scss',
                'scss/preloader.scss',
                'scss/text_styles.scss',

                'scss/popups/popups.scss',
                'scss/popups/preloader.scss',

                'popup_banner/scss/popup_banner.scss',
                'contacts/scss/block.scss',
                'footer/scss/footer.scss',
                'header/scss/header.scss',
                'menu/scss/menu.scss',
            ),
            'output_filename': 'css_build/head_core.css',
        },
        'admin_customize': {
            'source_filenames': (
                'admin/scss/admin_fixes.scss',
                'admin/scss/admin_table.scss',
                'admin/scss/button_filter.scss',
                'admin/scss/dl_core.scss',
                'admin/scss/dl_login.scss',
            ),
            'output_filename': 'admin/css/customize.css',
        },
        'main': {
            'source_filenames': PopupGallery.css + (
                'scss/section_slider.scss',
                'main/scss/index.scss',
            ),
            'output_filename': 'css_build/main.css',
        },
        'error': {
            'source_filenames': (
                'scss/error_page.scss',
            ),
            'output_filename': 'css_build/error.css',
        },
        'contacts': {
            'source_filenames': (
                'contacts/scss/index.scss',
            ),
            'output_filename': 'css_build/contacts.css',
        },
        'blog': {
            'source_filenames': (
                'paginator/scss/paginator.scss',
                'blog/scss/index.scss',
            ),
            'output_filename': 'css_build/blog.css',
        },
        'blog_detail': {
            'source_filenames': Slider.css + (
                'blog/scss/detail.scss',
            ),
            'output_filename': 'css_build/blog_detail.css',
        },
    },

    'JAVASCRIPT': {
        'core': {
            'source_filenames': (
                'polyfills/modernizr.js',
                'js/jquery-2.2.1.min.js',
                'js/jquery-ui-effects.js',

                'common/js/jquery.cookie.js',
                'common/js/jquery.utils.js',
                'common/js/jquery.ajax_csrf.js',

                'js/inspectors/inspector.js',
                'js/inspectors/bg_inspector.js',

                'js/jquery.fitvids.js',
                'js/jquery.scrollTo.js',

                'js/popups/jquery.popups.js',
                'js/popups/preloader.js',
                'js/text_styles.js',

                'attachable_blocks/js/async_blocks.js',
                'popup_banner/js/popup_banner.js',
                'ajax_cache/js/ajax_cache.js',
                'contacts/js/block.js',
                'menu/js/menu.js',
            ),
            'output_filename': 'js_build/core.js',
        },
        'main': {
            'source_filenames': PopupGallery.js + (
                'main/js/index.js',
            ),
            'output_filename': 'js_build/main.js',
        },
        'contacts': {
            'source_filenames': (
                'google_maps/js/core.js',
                'contacts/js/index.js',
            ),
            'output_filename': 'js_build/contacts.js',
        },
        'blog': {
            'source_filenames': (
                'blog/js/index.js',
            ),
            'output_filename': 'js_build/blog.js',
        },
        'blog_detail': {
            'source_filenames': Slider.js + (
                'blog/js/detail.js',
            ),
            'output_filename': 'js_build/blog_detail.js',
        },
    }
}