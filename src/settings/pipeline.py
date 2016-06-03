from ._pipeline import PIPELINE, PopupGallery, Slider

# ===============================
#   Скрипты
# ===============================

PIPELINE['STYLESHEETS'].update({
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

            'contacts/scss/block.scss',
            'footer/scss/footer.scss',
            'header/scss/header.scss',
            'menu/scss/menu.scss',
        ),
        'output_filename': 'css_build/head_core.css',
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
            'social_buttons/scss/social_buttons.scss',
            'blog/scss/detail.scss',
        ),
        'output_filename': 'css_build/blog_detail.css',
    },
})

PIPELINE['JAVASCRIPT'].update({
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
            'social_buttons/js/social_buttons.js',
            'blog/js/detail.js',
        ),
        'output_filename': 'js_build/blog_detail.js',
    },
})

