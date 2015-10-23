(function($) {

    $(document).ready(function() {
        // inlines
        window.formset = new Formset('#form .formset', {
            prefix: 'inlines'
        });

        $('#form').on('click', '.delete', function() {
            formset.deleteForm($(this).closest('.form'));
            return false;
        }).on('click', '.add', function() {
            formset.addForm();
            return false;
        });
    });

})(jQuery);
