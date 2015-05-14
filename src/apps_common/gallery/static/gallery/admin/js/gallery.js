(function($) {

    $(document).ready(function() {
        $('.gallery-standart').each(function() {
            var $self = $(this);
            if (!$self.closest('.empty-form').length) {
                $self.gallery();
            }
        });

        if (window.Suit) {
            Suit.after_inline.register('gallery', function (inline_prefix, row) {
                $(row).find('.gallery-standart').gallery();
            });
        }
    }).on('click.gallery', '.create-gallery', function() {
        var self = $(this),
            gallery = self.closest('.gallery').gallery('object');
        self.prop('disabled', true);
        gallery.create().always(function() {
            self.prop('disabled', false);
        });
        return false;
    }).on('click.gallery', '.delete-gallery', function() {
        var self = $(this),
            gallery = self.closest('.gallery').gallery('object');

        if (!confirm(gettext('Are you sure you want to delete this gallery?'))) {
            return false
        }

        self.prop('disabled', true);
        gallery.delete().always(function() {
            self.prop('disabled', false);
        });
        return false;
    }).on('click.gallery', '.add-gallery-video', function() {
        /* Добавление видео */
        var self = $(this),
            gallery = self.closest('.gallery').gallery('object');
        var video_link = prompt(gettext('Paste YouTube/Vimeo video URL'), 'http://');
        if (video_link) {
            gallery.addVideo(video_link);
        }
        return false;
    }).on('click.gallery', '.item-delete', function() {
        /* Удаление картинки */
        var self = $(this),
            gallery = self.closest('.gallery').gallery('object');

        gallery.deleteItem(self.closest('.gallery-item'));
        return false;
    }).on('click.gallery', '.item-rotate-left', function() {
        /* Поворот картинки против часовой стрелки */
        var self = $(this),
            gallery = self.closest('.gallery').gallery('object');

        gallery.rotateItem(self.closest('.gallery-item'), 'left').done(function() {
            self.closest('.gallery-item').find('.item-crop').removeData('crop');
        });
        return false;
    }).on('click.gallery', '.item-rotate-right', function() {
        /* Поворот картинки по часовой стрелке */
        var self = $(this),
            gallery = self.closest('.gallery').gallery('object');

        gallery.rotateItem(self.closest('.gallery-item'), 'right').done(function() {
            self.closest('.gallery-item').find('.item-crop').removeData('crop');
        });
        return false;
    });

})(jQuery);