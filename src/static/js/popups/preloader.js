(function() {

    /*
        Модальное окно с прелоадером

        Требует:
            jquery.utils.js, jquery.popups.js
     */

    $.preloader = function(options) {
        var opts = $.extend(true, {
            classes: 'popup-preloader',
            content: function() {
                var that = this;
                $.urlReader('/static/scss/popups/preloader.svg').done(function(content) {
                    that.$content.append(content);
                });
            },
            speed: 200,
            closeButton: false,
            hideOnClick: false
        }, options);

        var popup = OverlayedPopup.create(opts);
        return popup.show();
    };

})(jQuery);
