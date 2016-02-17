(function($) {

    $(document).on('input', '.file-on-page', function() {
        // генерация имени файла для отображения
        var self = $(this),
            short_name = /[^/\\]+$/.exec(self.val()),
            name_field = self.closest('.form-row').find('.file-on-page-name');

        name_field.val(short_name);
    });

})(jQuery);
