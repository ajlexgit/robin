(function($) {

    $(document).ready(function() {
        // inlines
        window.formset = Formset.create('#form .formset', {
            prefix: 'inlines'
        });

        $('#form').on('click', '.delete-inline', function() {
            formset.deleteForm($(this).closest('.form'));
            return false;
        }).on('click', '.add-inline', function() {
            formset.addForm();
            return false;
        });

        // custom checkboxes
        $('input:checkbox').each(function() {
            CustomCheckbox.create(this);
        });

        // custom counter
        $('.custom-counter').each(function() {
            CustomCounter.create(this);
        });
    });

})(jQuery);
