(function($) {

    $(document).on('submit', '#subscribe form', function() {
        var $form = $(this);

        $.ajax({
            url: window.js_storage.subscribe_url,
            type: 'POST',
            data: $form.serialize(),
            dataType: 'json',
            success: function(response) {
                $form.find('.invalid').removeClass('invalid');
                $form.get(0).reset();

                // TODO
                alert('Subscribed!');
            },
            error: $.parseError(function(response) {
                if (response && response.errors) {
                    response.errors.forEach(function(record) {
                        var $field = $form.find('.' + record.fullname);
                        $field.addClass(record.class);
                    })
                }
            })
        });

        return false;
    });

})(jQuery);