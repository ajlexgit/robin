(function() {

    /*
        Эффект параллакса при скролле.

        Требует:
            jquery.utils.js, jquery.popups.js
     */

    $.preloader = function(options) {
        var settings = $.extend({
            classes: 'preloader',
            content: function() {
                var that = this;
                $.urlReader('/static/scss/popups/preloader.svg').done(function(content) {
                    that.$content.append(content);
                });
            },
            ui: false,
            outClick: false
        }, options);
        return $.popup.force(settings);
    };

})(jQuery);
