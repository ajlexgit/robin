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
                }
            },
            error: $.parseError(function() {
                alert(window.DEFAULT_AJAX_ERROR);
                $.popup().hide();
            })
        });
    };


    /*
        Открытие окна контактов при клике на кнопки
     */
    $(document).on('click', '.open-contact-popup', function() {
        contactPopup();
        return false;
    });


    /*
        Отправка AJAX-формы
     */
    $(document).on('submit', '#ajax-contact-form', function() {
        var $form = $(this);
        if ($form.hasClass('sending')) {
            return false;
        }

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
            beforeSend: function() {
                $form.addClass('sending');
                $form.find('.invalid').removeClass('invalid');
            },
            success: function(response) {
                if (response.success_message) {
                    // сообщение о успешной отправке
                    $.popup({
                        classes: 'contact-popup contact-success-popup',
                        content: response.success_message
                    }).show();

                    $form.get(0).reset();
                }
            },
            error: $.parseError(function(response) {
                if (response && response.errors) {
                    // ошибки формы
                    response.errors.forEach(function(record) {
                        var $field = $form.find('.' + record.fullname);
                        if ($field.length) {
                            $field.addClass(record.class);
                        }
                    });
                } else {
                    alert(window.DEFAULT_AJAX_ERROR);
                    $.popup().hide();
                }
            }),
            complete: function() {
                $form.removeClass('sending');
            }
        });

        return false;
    });

})(jQuery);
