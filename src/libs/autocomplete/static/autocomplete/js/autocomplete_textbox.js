(function($) {

    var bind_autocomplete_text_widget = function(elements) {
        elements.each(function() {
            var self = $(this),
                choices = self.next('.choices').children();

            var tags = [];
            choices.each(function() {
                var value = $.trim($(this).text());
                if (value) {
                    tags.push(value);
                }
            });

            self.select2({
                tags: tags,
                tokenSeparators: [],
                maximumInputLength: parseInt(self.attr('maxlength')) || null,
                maximumSelectionSize: 1
            });
        })
    };


    $(document).ready(function() {
        $('.autocomplete_textbox_widget').each(function() {
            var self = $(this);
            if (!self.closest('.empty-form').length) {
                bind_autocomplete_text_widget(self);
            }
        });

        if (window.Suit) {
            Suit.after_inline.register('autocomplete_textbox_widget', function(inline_prefix, row) {
                bind_autocomplete_text_widget(row.find('.autocomplete_textbox_widget'));
            });
        }
    });

})(jQuery);
