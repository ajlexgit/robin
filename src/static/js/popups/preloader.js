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
                var $preloader = $('<div>').addClass('preloader');
                this.$content.append($preloader);
            },
            closeButton: false,
            hideOnClick: false
        }, options);

        var popup = OverlayedPopup(opts);
        return popup && popup.show();
    };

})(jQuery);
