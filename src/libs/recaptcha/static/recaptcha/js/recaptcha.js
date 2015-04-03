(function($) {

    // Инициализация капчи с сохранением виджета
    window.initReCaptcha = function(element) {
        var self_data = $(element).data();
        return self_data.widget = grecaptcha.render(element, self_data);
    };

    // Инициализация всех капч на странице
    // https://developers.google.com/recaptcha/docs/display#js_api
    window.recaptchaLoadCallback = function() {
        $(document).ready(function() {
            $('.g-recaptcha').each(function() {
                window.initReCaptcha(this);
            });
        });
    };

})(jQuery);