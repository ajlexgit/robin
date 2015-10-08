(function() {

    /*
        Превращение формы в AJAX-форму.

        Автоматически блокируется попытка одновременной
        отправки нескольких экземпляров формы.

        URL и метод (GET/POST) по умолчанию берутся из аттрибутов формы.

        Параметры аналогичны параметрам $.ajax, за исключением того,
        что добавлен метод modifyData, принимающий объект данных формы,
        который может его модифицировать.
     */

    // Получение данных формы в виде объекта
    var buildFormData = function($form) {
        var data_array = $form.serializeArray();
        var form_data = {};
        for (var i = 0, l = data_array.length; i < l; i++) {
            var form_field = data_array[i];
            form_data[form_field.name] = form_field.value;
        }
        return form_data;
    };

    // Обработчик отправки форм
    var onSubmit = function(settings) {
        var $form = $(this);
        if ($form.data('ajaxform_blocked')) {
            return false;
        }

        var form_data = buildFormData($form);
        var data = settings.modifyData(form_data);

        $.ajax($.extend({
            data: data
        }, settings));

        return false;
    };


    $.fn.ajaxForm = function(options) {
        options = options || {};
        return this.each(function() {
            var $form = $.findFirstElement(this);
            if (!$form.length) {
                console.error('AjaxForm: element is empty');
                return
            }
            if ($form.prop('tagName') != 'FORM') {
                console.error('AjaxForm: element is not a form');
                return
            }

            var settings = $.extend(true, {
                url: $form.attr('action'),
                type: $form.attr('method'),
                dataType: 'json',
                modifyData: function(data) {
                    return data
                }
            }, options, {
                beforeSend: function() {
                    $form.data('ajaxform_blocked', true);
                    if (options.beforeSend && $.isFunction(options.beforeSend)) {
                        options.beforeSend.apply(this, arguments);
                    }
                },
                complete: function() {
                    $form.data('ajaxform_blocked', false);
                    if (options.complete && $.isFunction(options.complete)) {
                        options.complete.apply(this, arguments);
                    }
                }
            });

            $form.off('.ajax-form').on('submit.ajax-form', function() {
                return onSubmit.call(this, settings);
            });
        });
    };

})(jQuery);
