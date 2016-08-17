(function($) {

    $(document).on('submit', '#subscribe-form', function() {
        var $form = $(this);
        if ($form.hasClass('sending')) {
            return false;
        } else {
            $form.addClass('sending');
        }

        $.ajax({
            url: window.js_storage.subscribe_url,
            type: 'POST',
            data: $form.serialize(),
            dataType: 'json',
            beforeSend: function() {
                $form.find('.invalid').removeClass('invalid');
            },
            success: function(response) {
                $form.get(0).reset();

                if (response.success_message) {
                    $.popup({
                        classes: 'subscribe-popup subscribe-success-popup',
                        content: response.success_message
                    }).show();
                }
            },
            error: $.parseError(function(response) {
                if (response && response.errors) {
                    response.errors.forEach(function(record) {
                        var $field = $form.find('.' + record.fullname);
                        $field.addClass(record.class);
                    })
                }
            }),
            complete: function() {
                $form.removeClass('sending');
            }
        });

        return false;
    });

})(jQuery);