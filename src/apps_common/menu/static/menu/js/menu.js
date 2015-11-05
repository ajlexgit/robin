(function($) {

    /*

        Требует:
            jquery.utils.js

    */

    var refresh_menu = function() {
        var $menu = $('#main-menu');
        if (!$menu.hasClass('active')) {
            return
        }

        if (window.innerWidth < 1024) {
            // На мобиле и iPad высота меню - весь экран
            $.winHeight($menu);
        } else {
            $('#mobile-menu-button').removeClass('active');
            $menu.removeClass('active');
        }
    };

    $(document).ready(function() {
        // Клик на кнопку мобильного меню
        $('#mobile-menu-button').on('click', function() {
            var $button = $(this);
            var $menu = $('#main-menu');
            if ($button.hasClass('active')) {
                $button.removeClass('active');
                $menu.removeClass('active');
            } else {
                $button.addClass('active');
                $menu.addClass('active');
                refresh_menu();
            }
        });
    });

    $(window).on('resize', $.rared(refresh_menu, 150));

})(jQuery);
