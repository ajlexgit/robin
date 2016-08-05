(function($) {

    $(document).on('change', '.file-on-page', function() {
        var $input = $(this);
        var formset_prefix = $input.attr('name').split('-').slice(0, -1).join('-');
        var $name = $('#id_' + formset_prefix + '-name');

        console.log();
        if ($name.val()) return;

        var short_name = /[^/\\]+$/.exec($input.val());
        if (short_name) {
            $name.val(short_name);
        }
    });

})(jQuery);
