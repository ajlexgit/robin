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
            success: function() {
                $form.get(0).reset();

                $.popup({
                    content: '<h1>You have successfully subscribed to the newsletter!</h1>'
                }).show();
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