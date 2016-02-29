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
                var popup = $.popup({
                    classes: 'contact-popup contact-form-popup',
                    content: response
                }).show();

                InitContactPopup(popup.$content.find('form'));
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
    var InitContactPopup = function($form) {
        $form.ajaxForm({
            url: window.js_storage.ajax_contact,
            dataType: 'json',
            beforeSubmit: function(arr, $form, options) {
                $.preloader();

                arr.push({
                    name: 'referer',
                    value: location.href
                });
            },
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

                    InitContactPopup(popup.$content.find('form'));
                } else {
                    alert(window.DEFAULT_AJAX_ERROR);
                    $.popup().hide();
                }
            })
        });
    };


    /*
        Открытие окна контактов при клике на кнопки
     */
    $(document).on(touchClick, '.open-contact-popup', function() {
        contactPopup();
        return false;
    });

})(jQuery);
