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