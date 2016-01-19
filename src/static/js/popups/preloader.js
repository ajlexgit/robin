(function() {

    /*
        Модальное окно с прелоадером.
        Возвращает Deferred-объект анимации показа.

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
            closeButton: false,
            hideOnClick: false
        }, options);

        var popup = OverlayedPopup(opts);
        return popup.show();
    };

})(jQuery);
