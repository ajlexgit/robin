(function($) {

    /*
        Отключение :hover-эффектов при скроллинге страницы
        http://habrahabr.ru/post/204238
    */

    var timer;
    $(window).on('scroll', function() {
        clearTimeout(timer);
        if (document.body.style.pointerEvents != 'none') {
            document.body.style.pointerEvents = 'none'
        }
        timer = setTimeout(function() {
            document.body.style.pointerEvents = ''
        }, 300)
    })

})(jQuery);
