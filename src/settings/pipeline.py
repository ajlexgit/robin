from ._pipeline import PIPELINE


PIPELINE['STYLESHEETS'].update({
    'critical': {
        'source_filenames': (
            'scss/grid.scss',
            'scss/layout.scss',
            'scss/buttons.scss',

            'header/scss/header.scss',
            'menu/scss/main_menu.scss',
        ),
        'output_filename': 'css_build/critical.css',
    },
    'core': {
        'source_filenames': (
            'scss/forms.scss',
            'scss/preloader.scss',
            'scss/text_styles.scss',

            'scss/popups/popups.scss',
            'scss/popups/preloader.scss',

            'contacts/scss/block.scss',
            'footer/scss/footer.scss',
        ),
        'output_filename': 'css_build/head_core.css',
    },
    'error': {
        'source_filenames': (
            'scss/error_page.scss',
        ),
        'output_filename': 'css_build/error.css',
    },
    'main': {
        'source_filenames': (
            'main/scss/index.scss',
        ),
        'output_filename': 'css_build/main.css',
    },
    'contacts': {
        'source_filenames': (
            'google_maps/scss/label.scss',
            'contacts/scss/index.scss',
        ),
        'output_filename': 'css_build/contacts.css',
    },
})

PIPELINE['JAVASCRIPT'].update({
    'core': {
        'source_filenames': (
            'polyfills/modernizr.js',
            'js/jquery-2.2.4.js',
            'js/jquery-ui.min.js',
            'js/jquery.requestanimationframe.js',

            'common/js/jquery.cookie.js',
            'common/js/jquery.utils.js',
            'common/js/jquery.ajax_csrf.js',

            'js/popups/jquery.popups.js',
            'js/popups/preloader.js',
            'js/jquery.inspectors.js',
            'js/jquery.fitvids.js',
            'js/text_styles.js',

            'attachable_blocks/js/async_blocks.js',
            'placeholder/js/placeholder.js',
            'contacts/js/popup.js',
            'menu/js/main_menu.js',
        ),
        'output_filename': 'js_build/core.js',
    },
    'main': {
        'source_filenames': (
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
})

