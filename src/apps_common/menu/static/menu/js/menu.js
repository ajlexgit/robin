(function($) {

    var refresh_menu = function() {
        var $menu = $('#main-menu');
        if (!$menu.hasClass('active')) {
            return
        }

        if (window.innerWidth < 1024) {
            var win_height = $(window).innerHeight();
            $menu.outerHeight(win_height);
        } else {
            $('#mobile-menu').removeClass('active');
            $menu.removeClass('active');
        }
    };

    $(document).ready(function() {
        // Клик на кнопку мобильного меню
        $('#mobile-menu').on('click', function() {
           var self = $(this);
           var menu = $('#main-menu');
           if (self.hasClass('active')) {
               self.removeClass('active');
               menu.removeClass('active');
           } else {
               self.addClass('active');
               menu.addClass('active');
               refresh_menu();
           }
        });
    });

    $(window).on('resize', $.rared(refresh_menu, 150));

})(jQuery);