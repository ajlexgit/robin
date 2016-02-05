(function($) {

    $(document).on('click', '.comment-delete', function() {
        // Ссылка удаления комментария
        var button = $(this);
        $.ajax({
            url: window.admin_comments_delete,
            type: 'POST',
            data: {
                id: button.data('id')
            },
            success: function() {
                button
                    .addClass('disabled')
                    .prop('disabled', true)
                    .closest('td')
                    .siblings('.field-restore')
                    .find('button')
                    .removeClass('disabled')
                    .prop('disabled', false);
            },
            error: $.parseError()
        });
        return false;
    }).on('click', '.comment-restore', function() {
        // Ссылка восстановления комментария
        var button = $(this);
        $.ajax({
            url: window.admin_comments_restore,
            type: 'POST',
            data: {
                id: button.data('id')
            },
            success: function() {
                button
                    .addClass('disabled')
                    .prop('disabled', true)
                    .closest('td')
                    .siblings('.field-delete')
                    .find('button')
                    .removeClass('disabled')
                    .prop('disabled', false);
            },
            error: $.parseError()
        });
        return false;
    })

})(jQuery);
