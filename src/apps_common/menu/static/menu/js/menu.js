(function($) {

    /*

        Требует:
            rared.js, win_height.js

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
            $('#mobile-menu').removeClass('active');
            $menu.removeClass('active');
        }
    };

    $(document).ready(function() {
        // Клик на кнопку мобильного меню
        $('#mobile-menu').on('click', function() {
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