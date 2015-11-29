(function($) {

    $(document).ready(function() {
        $('.async-block').each(function() {
            var $block = $(this);
            $.ajax({
                url: $block.data('url'),
                type: 'POST',
                data: {
                    referrer: location.toString()
                },
                dataType: 'json',
                success: function(response) {
                    $block.replaceWith(response.html);
                    $block.trigger('loaded.async_block');
                },
                error: function() {
                    $block.remove();
                }
            });
        });
    });

})(jQuery);
