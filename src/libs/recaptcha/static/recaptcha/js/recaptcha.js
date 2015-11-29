(function($) {

    // Инициализация капчи с сохранением виджета
    window.initRecaptcha = function(element) {
        var self_data = $(element).data();
        return self_data.widget = grecaptcha.render(element, self_data);
    };

    // Инициализация всех капч на странице
    // https://developers.google.com/recaptcha/docs/display#js_api
    $(document).on('recaptcha-ready', function() {
        $('.g-recaptcha').each(function() {
            window.initRecaptcha(this);
        });
    });


    window.init_recaptcha = function() {
        $(document).trigger('recaptcha-ready');
    };

    $(document).ready(function() {
        var lang = $(document.documentElement).attr('lang');
        var script = document.createElement('script');
        script.src = 'https://www.google.com/recaptcha/api.js?onload=init_recaptcha&render=explicit&lang=' + lang;
        document.body.appendChild(script);
    });

})(jQuery);
