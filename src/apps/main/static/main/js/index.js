(function($) {

    $(document).on('appear', '.appear-block', function () {
        $(this).addClass('visible');
    });

    $(document).ready(function() {
        $('#video').winHeight().videoBackground();

        $('.appear-block').appear();
        $.force_appear();
    });

})(jQuery);