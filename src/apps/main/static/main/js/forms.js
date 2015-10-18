(function($) {

    $(document).ready(function() {
        // inlines
        window.formset = new Formset('#form .formset', {
            prefix: 'inlines'
        });

        $('#form').on('click', '.delete', function() {
            formset.deleteForm($(this).closest('.form'), true);
            return false;
        }).on('click', '.add', function() {
            formset.addForm();
            return false;
        });
    });

})(jQuery);
