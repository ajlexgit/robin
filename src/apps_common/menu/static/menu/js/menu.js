(function($) {

    // Клик на кнопку мобильного меню
    $(document).ready(function() {
        $('#mobile-menu').on('click', function() {
           var self = $(this);
           var menu = $('#main-menu');
           if (self.hasClass('active')) {
               self.removeClass('active');
               menu.removeClass('active');
           } else {
               self.addClass('active');
               menu.addClass('active');
           }
        });
    });

})(jQuery);