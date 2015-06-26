(function($) {

    var format_color = function(value) {
        value = value.toString().trim();

        if (value) {
            if (value[0] != '#') {
                value = '#' + value;
            }
        }

        if (value.length == 4) {
            var i = 0;
            var result = '#';
            var char;
            while (char = value.charAt(++i)) {
                result += char + char;
            }
            return result.toUpperCase();
        } else if (value.length == 7) {
            return value.toUpperCase();
        } else {
            return '#000000'
        }
    };

    $(document).on('change', '.colorfield-input', function() {
        // Изменение цвета в input[color]
        $(this).siblings('.colorfield-text').val(this.value.toUpperCase())
    }).on('keyup', '.colorfield-text', function() {
        // Изменение цвета в input[text]
        var self = $(this);
        var value = format_color(self.val());
        self.siblings('.colorfield-input').val(value);
    }).on('focusout', '.colorfield-text', function() {
        // Завершение редактирования цвета в input[text]
        var self = $(this);
        var value = format_color(self.val());
        self.val(value);
        self.siblings('.colorfield-input').val(value);
    });

})(jQuery);