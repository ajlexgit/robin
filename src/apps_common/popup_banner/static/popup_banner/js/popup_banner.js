(function($) {

    var BannerPopup = Class(OverlayedPopup, function BannerPopup(cls, superclass) {
        cls.defaults = $.extend({}, superclass.defaults, {
            hideOnClick: false
        });

        cls.CONTAINER_ID = 'popup-banner-container';
        cls.OVERLAY_ID = 'popup-banner-overlay';
    });


    /*
        Показ окна баннера
     */
    window.bannerPopup = function() {
        var cookie_name = 'banner_' + window.js_storage.popup_banner_id;
        var show_type = window.js_storage.popup_show_type;
        var was_shown = $.cookie(cookie_name);

        $.removeCookie(cookie_name);
        if (show_type == SHOW_ONCE_SESSION) {
            $.cookie(cookie_name, 1);
        } else if (show_type == SHOW_ONCE) {
            $.cookie(cookie_name, 1, {
                expires: 180
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
                        classes: 'banner-popup',
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