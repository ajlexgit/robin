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
        'main_page': {
            'source_filenames': (
                'scss/slider/slider.scss',
                'scss/slider/plugins/controls.scss',
                'scss/slider/plugins/navigation.scss',

                'scss/section_slider.scss',
                'gallery/scss/gallery_popup.scss',
                'main/scss/index.scss',
            ),
            'output_filename': 'css_build/main_page.css',
        },
        'error_page': {
            'source_filenames': (
                'scss/error_page.scss',
            ),
            'output_filename': 'css_build/error_page.css',
        },
        'contacts_page': {
            'source_filenames': (
                'contacts/scss/index.scss',
            ),
            'output_filename': 'css_build/contacts_page.css',
        },
        'blog_page': {
            'source_filenames': (
                'paginator/scss/paginator.scss',
                'blog/scss/index.scss',
            ),
            'output_filename': 'css_build/blog_page.css',
        },
        'blog_detail_page': {
            'source_filenames': (
                'blog/scss/detail.scss',
            ),
            'output_filename': 'css_build/blog_detail_page.css',
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
                'ajax_cache/js/ajax_cache.js',
                'contacts/js/block.js',
                'menu/js/menu.js',
            ),
            'output_filename': 'js_build/core.js',
        },
        'main_page': {
            'source_filenames': (
                'js/drager.js',
                'js/jquery.youtube.js',
                'js/jquery.vimeo.js',

                'js/slider/slider.js',
                'js/slider/win_height_slider.js',
                'js/slider/plugins/side_animation.js',
                'js/slider/plugins/fade_animation.js',
                'js/slider/plugins/autoscroll.js',
                'js/slider/plugins/navigation.js',
                'js/slider/plugins/controls.js',
                'js/slider/plugins/drag.js',

                'gallery/js/gallery_popup.js',
                'main/js/index.js',
            ),
            'output_filename': 'js_build/main_page.js',
        },
        'contacts_page': {
            'source_filenames': (
                'google_maps/js/core.js',
                'contacts/js/index.js',
            ),
            'output_filename': 'js_build/contacts_page.js',
        },
        'blog_page': {
            'source_filenames': (
                'blog/js/index.js',
            ),
            'output_filename': 'js_build/blog_page.js',
        },
        'blog_detail_page': {
            'source_filenames': (
                'blog/js/detail.js',
            ),
            'output_filename': 'js_build/blog_detail_page.js',
        },
    }
}