(function($) {
    
    $(document).ready(function() {
        $('.async-block').each(function() {
            var self = $(this);
            $.ajax({
                url: self.data('url'),
                type: 'POST',
                data: {
                    referrer: location.toString()
                },
                success: function(response) {
                    self.replaceWith(response);
                    self.trigger('loaded.async_block');
                },
                error: function() {
                    self.remove();
                }
            });
        });
    });

})(jQuery);