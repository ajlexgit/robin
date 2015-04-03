(function($) {

    // Устанавливаем CSRF-токен всем AJAX-запросам
    $(document).ajaxSend(function(event, xhr, settings) {
        if (!/^https?:\/\//i.test(settings.url)) {
            xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
        }
    });

})(jQuery);
