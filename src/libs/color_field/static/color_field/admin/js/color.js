(function($) {

    $(document).on('change', '.colorfield-input', function() {
        $(this).siblings('.colorfield-text').val(this.value.toUpperCase())
    });

    // Изменение текстового представления
    $(document).on('keyup change', '.colorfield-text', function() {
        var self = $(this),
            value = self.val().trim();

        if (value[0] != '#') {
            value = '#' + value;
        }
        self.siblings('.colorfield-input').val(value);
    });

    // Завершение редактирования текстового представления
    $(document).on('focusout', '.colorfield-text', function() {
        var self = $(this),
            value = self.val().trim();

        if (value) {
            if (value[0] != '#') {
                value = '#' + value;
            }
            value = value.toUpperCase();
            self.siblings('.colorfield-input').val(value);
        }
        self.val(value);
    });

})(jQuery);