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
                success: function(response) {
                    $block.replaceWith(response);
                    $block.trigger('loaded.async_block');
                },
                error: function() {
                    $block.remove();
                }
            });
        });
    });

})(jQuery);
