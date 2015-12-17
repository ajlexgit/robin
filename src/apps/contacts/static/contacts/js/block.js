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
                    classes: 'contacts-popup',
                    content: response
                }).show();
            },
            error: function() {
                alert(gettext('Connection error'));
                $.popup().hide();
            }
        });
    };

    $(document).on('click', '.contact-popup', function() {
        // Открытие окна контактов
        contactPopup();
        return false;
    }).on('submit', '#ajax-contact-form', function() {
        // Отправка Ajax-формы контактов
        $.preloader();

        // Add referer
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
                        classes: 'contacts-popup',
                        content: response.form
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
