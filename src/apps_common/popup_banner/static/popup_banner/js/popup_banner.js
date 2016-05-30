(function($) {

    /*
        Треует:
            bg_inspector.js, popups.js
     */

    var SHOW_ALWAYS = 'always';
    var SHOW_ONCE_SESSION = 'session';
    var SHOW_ONCE = 'once';


    var BannerPopup = Class(OverlayedPopup, function BannerPopup(cls, superclass) {
        cls.defaults = $.extend({}, superclass.defaults, {
            hideOnClick: false
        });

        cls.OVERLAY_ID = 'popup-banner-overlay';

        cls.extraDOM = function() {
            superclass.extraDOM.call(this);
            $.bgInspector.inspect(this.$content.find('.image'));
        };

        cls._removeDOM = function() {
            superclass._removeDOM.call(this);
            $.bgInspector.ignore(this.$content.find('.image'));
        };
    });


    /*
        Показ окна баннера
     */
    window.bannerPopup = function() {
        if (getCurrentPopup()) {
            console.info('Banner popup was blocked because another popup is opened');
            return;
        }

        var cookie_name = 'banner_' + window.js_storage.popup_banner_id;
        var show_type = window.js_storage.popup_show_type;
        var was_shown = $.cookie(cookie_name);

        $.removeCookie(cookie_name);
        if (show_type == SHOW_ONCE_SESSION) {
            $.cookie(cookie_name, 1);
        } else if (show_type == SHOW_ONCE) {
            $.cookie(cookie_name, 1, {
                expires: 180,
                path: '/'
            });
        }

        if (was_shown && (show_type != SHOW_ALWAYS)) {
            return
        }

        return $.ajax({
            url: window.js_storage.ajax_popup_banner,
            type: 'GET',
            data: {
                banner: window.js_storage.popup_banner_id
            },
            dataType: 'json',
            success: function(response) {
                if (response.html) {
                    var popup = BannerPopup({
                        classes: 'popup-banner',
                        content: response.html
                    }).show();
                }
            }
        });
    };

    $(document).ready(function() {
        var timeout = window.js_storage.popup_banner_timeout;
        if (!timeout) return;

        setTimeout(bannerPopup, timeout * 1000);
    })

})(jQuery);