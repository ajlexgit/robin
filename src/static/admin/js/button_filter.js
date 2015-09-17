(function($) {

    $(document).on('change', '.button-filter input', function() {
        $(this).closest('.btn').addClass('active').siblings('.active').removeClass('active');
    });

})(jQuery);
