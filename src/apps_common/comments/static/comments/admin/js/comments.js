(function($) {
    
    $(document).on('click', '.comment-delete', function() {
        var button = $(this);
        $.ajax({
            url: window.admin_comments_delete,
            type: 'POST',
            data: {
                'id': button.data('id'),
            },
            success: function(response) {
                if (response.error) {
                    alert(response.error);
                    return;
                }
                button
                    .addClass('disabled')
                    .prop('disabled', true)
                    .closest('td')
                        .siblings('.field-restore')
                            .find('button')
                            .removeClass('disabled')
                            .prop('disabled', false);
            }
        });
        return false;
    });
    
    
    $(document).on('click', '.comment-restore', function() {
        var button = $(this);
        $.ajax({
            url: window.admin_comments_restore,
            type: 'POST',
            data: {
                'id': button.data('id'),
            },
            success: function(response) {
                if (response.error) {
                    alert(response.error);
                    return;
                }
                button
                    .addClass('disabled')
                    .prop('disabled', true)
                    .closest('td')
                        .siblings('.field-delete')
                            .find('button')
                            .removeClass('disabled')
                            .prop('disabled', false);
            }
        });
        return false;
    })
    
})(jQuery);
