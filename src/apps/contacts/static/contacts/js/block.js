(function($) {

    /*
        Показ окна контактов
     */
    window.contactPopup = function() {
        $.preloader();

        return $.ajax({
            url: window.js_storage.ajax_contact,
            type: 'GET',
            dataType: 'json',
            success: function(response) {
                if (response.form) {
                    var popup = $.popup({
                        classes: 'contact-popup contact-form-popup',
                        content: response.form
                    }).show();

                    InitContactPopup(popup);
                }
            },
            error: function() {
                alert(window.DEFAULT_AJAX_ERROR);
                $.popup().hide();
            }
        });
    };

    /*
        Инициализация окна контактов
     */
    var InitContactPopup = function(popup) {
        var $form = popup.$content.find('form');

        $form.on('submit', function() {
            $.preloader();

            // добавление адреса страницы, откуда отправлена форма
            var data = $(this).serializeArray();
            data.push({
                name: 'referer',
                value: location.href
            });

            $.ajax({
                url: window.js_storage.ajax_contact,
                type: 'post',
                data: data,
                dataType: 'json',
                success: function(response) {
                    if (response.success_message) {
                        // сообщение о успешной отправке
                        $.popup({
                            classes: 'contact-popup contact-success-popup',
                            content: response.success_message
                        }).show();
                    }
                },
                error: $.parseError(function(response) {
                    if (response && response.form) {
                        // ошибки формы
                        var popup = $.popup({
                            classes: 'contact-popup contact-form-popup',
                            content: response.form
                        }).show();

                        InitContactPopup(popup);
                    } else {
                        alert(window.DEFAULT_AJAX_ERROR);
                        $.popup().hide();
                    }
                })
            });

            return false;
        });
    };


    /*
        Открытие окна контактов при клике на кнопки
     */
    $(document).on('click', '.open-contact-popup', function() {
        contactPopup();
        return false;
    });

})(jQuery);
