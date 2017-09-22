from ._pipeline import PIPELINE, Slider


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
            'social_networks/scss/social_links.scss',
        ),
        'output_filename': 'css_build/head_core.css',
    },
    'error': {
        'source_filenames': (
            'scss/error_page.scss',
        ),
        'output_filename': 'css_build/error.css',
    },
    'fonts': {
        'source_filenames': (
            'fonts/alice/stylesheet.css',
            'fonts/playfair/stylesheet.css',
        ),
        'output_filename': 'css_build/fonts.css',
    },
    'main': {
        'source_filenames': Slider.css + (
            'main/scss/index.scss',
            'robin/scss/index.scss',
            'robin/scss/media-robin.scss',
        ),
        'output_filename': 'css_build/main.css',
    },
    'robin': {       #спросить
        'source_filenames': (
            'robin/scss/index.scss',
        ),
        'output_filename': 'css_build/robin.css',
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
            'js/jquery-ui.js',
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
            'contacts/js/popups.js',
            'menu/js/main_menu.js',
        ),
        'output_filename': 'js_build/core.js',
    },
    'main': {
        'source_filenames': Slider.js + (
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

