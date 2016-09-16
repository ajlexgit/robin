(function($) {

    $(document).on('change', '.file-widget input', function() {
        var $input = $(this);
        var $widget = $input.closest('.file-widget');
        $widget.removeClass('has-value');
    });

})(jQuery);
