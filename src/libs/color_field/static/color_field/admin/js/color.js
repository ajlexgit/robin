(function($) {

    var color_regex = /^#?([0-9a-f]{3}|[0-9a-f]{6})$/i;

    var format_color = function(value) {
        var hex;

        value = value.toString().trim();
        if (!(hex = color_regex.exec(value))) {
            return ''
        }

        hex = hex[1];
        if (hex.length == 6) {
            return '#' + hex.toUpperCase();
        } else {
            var i = 0;
            var result = '#';
            var char;
            while (char = hex.charAt(i++)) {
                result += char + char;
            }
            return result.toUpperCase();
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
