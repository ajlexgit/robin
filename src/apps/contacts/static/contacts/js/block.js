(function($) {

    /*
        Показ окна контактов
     */
    window.contactPopup = function() {
        $.preloader();

        return $.ajax({
            url: window.js_storage.ajax_contact,
            type: 'GET',
            success: function(response) {
                $.popup({
                    classes: 'contact-popup contact-form-popup',
                    content: response
                }).show();
            },
            error: function() {
                alert(gettext('Connection error'));
                $.popup().hide();
            }
        });
    };

    $(document).on(touchClick, '.open-contact-popup', function() {
        // Открытие окна контактов
        contactPopup();
        return false;
    }).on('submit', '#ajax-contact-form', function() {
        // Отправка Ajax-формы контактов
        $.preloader();

        // Добавляем адрес страницы, с которой отправили сообщение
        var $form = $(this);
        var data = $form.serializeArray();
        data.push({
            name: 'referer',
            value: location.href
        });

        $.ajax({
            url: window.js_storage.ajax_contact,
            type: 'POST',
            data: data,
            dataType: 'json',
            success: function(response) {
                if (response.errors) {
                    // ошибки формы
                    $.popup({
                        classes: 'contact-popup contact-form-popup',
                        content: response.form
                    }).show();
                } else if (response.success_message) {
                    // сообщение о успешной отправке
                    $.popup({
                        classes: 'contact-popup contact-success-popup',
                        content: response.success_message
                    }).show();
                } else {
                    $.popup().hide();
                }
            },
            error: function() {
                alert(gettext('Connection error'));
                $.popup().hide();
            }
        });
        return false;
    });

})(jQuery);
