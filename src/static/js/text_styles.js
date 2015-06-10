(function($) {

    /*
        Требует:
            jquery.rared.js, jquery.fitvids.js, jquery.responsiveinstagram.js
    */

    var fixInstagram = function() {
        $('iframe[src*="instagram.com"]').responsiveInstagram();
    };

    $(document).ready(function() {
        // Видео на всю ширину с сохранение пропорций
        $('.page-video').fitVids();

        fixInstagram();
    });

    $(window).on('load', function() {
        fixInstagram();
    }).on('resize', $.rared(fixInstagram));

})(jQuery);