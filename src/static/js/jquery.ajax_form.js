(function() {

    /*
        Превращение формы в AJAX-форму.

        Автоматически блокируется попытка одновременной
        отправки нескольких экземпляров формы.

        Параметры аналогичны параметрам $.ajax;
     */

    var onSubmit = function(settings) {
        var $form = $(this);
        if ($form.data('ajaxform_blocked')) {
            return false;
        }

        var default_data = $form.serialize();
        $.ajax($.extend({
            data: default_data
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
                dataType: 'json'
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
