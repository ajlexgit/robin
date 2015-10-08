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

    var re_split_name = /^([^\[\]]+)(\[.*])?$/;     // "x[][name][5]"  =>  [..., "x", "[][5]"]
    var re_brackets = /\[.*?]/g;    // "[][name][5]"  => ["[]", "[name]", "[5]"]

    var buildFormData = function($form) {
        var data_array = $form.serializeArray();
        var form_data = {};
        for (var i = 0, l = data_array; i < l; i++) {
            var form_field = data_array[i];

            var arr = re_split_name.exec(form_field.name);
            if (!arr) {
                console.error('buildFormData: bad field name "' + form_field.name + '"');
                continue
            }

            var name = arr[1];
            var params = arr[2];

            form_data[name] = form_field.value;
        }
    };


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
                    this.$form = $form;
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
