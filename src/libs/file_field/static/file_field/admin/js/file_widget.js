(function($) {

    $(document).on('change', '.file-widget input', function() {
        var $input = $(this);
        var $widget = $input.closest('.file-widget');

        var file = this.files[0];
        if (file) {
            // выбран новый файл
            $widget.addClass('has-value').removeClass('has-link');
            $widget.find('label').find('span').text(file.name);
        } else {
            // возврат исходного состояния
            var old_name = $widget.data('old-name');
            if (old_name) {
                $widget.addClass('has-value has-link');
                $widget.find('label').find('span').text(old_name);
            } else {
                $widget.removeClass('has-value');
                $widget.find('label').find('span').text(gettext('Choose a file'));
            }
        }
    });

    $(document).ready(function() {
        $('.file-widget').each(function() {
            if (!$(this).closest('.empty-form').length) {
                FileDropper(this);
            }
        });

        if (window.Suit) {
            Suit.after_inline.register('file-widget', function(inline_prefix, row) {
                row.find('.file-widget').each(function() {
                    FileDropper(this);
                });
            });
        }
    });

})(jQuery);
