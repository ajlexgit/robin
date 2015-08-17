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
            $item = self.closest('.gallery-item'),
            gallery = self.closest('.gallery').gallery('object');

        gallery.deleteItem($item);
        return false;
    }).on('click.gallery', '.item-rotate-left', function() {
        /* Поворот картинки против часовой стрелки */
        var self = $(this),
            $item = self.closest('.gallery-item'),
            gallery = self.closest('.gallery').gallery('object');

        gallery.rotateItem($item, 'left').done(function() {
            $item.find('.item-crop').removeData('crop');
        });
        return false;
    }).on('click.gallery', '.item-rotate-right', function() {
        /* Поворот картинки по часовой стрелке */
        var self = $(this),
            $item = self.closest('.gallery-item'),
            gallery = self.closest('.gallery').gallery('object');

        gallery.rotateItem($item, 'right').done(function() {
            $item.find('.item-crop').removeData('crop');
        });
        return false;
    }).on('click.gallery', '.item-description', function() {
        /* Редактирвоание описания картинки */
        var self = $(this),
            $item = self.closest('.gallery-item'),
            gallery = self.closest('.gallery').gallery('object');

        var $template = $('<div>')
            .attr('id', 'description-dialog')
            .append('<textarea>')
            .appendTo('body');

        gallery.getItemDescription($item).done(function(response) {
            $template.find('textarea').val(response.description);

            var dialog = $template.dialog({
                title: gettext('Set description'),
                width: 540,
                closeText: '',
                show: {
                    effect: "fadeIn",
                    duration: 100
                },
                hide: {
                    effect: "fadeOut",
                    duration: 100
                },
                modal: true,
                resizable: false,
                position: {
                    my: "center center",
                    at: "center center",
                    of: window
                },
                buttons: [
                    {
                        text: gettext('Cancel'),
                        click: function() {
                            $(this).dialog('close');
                        }
                    },
                    {
                        text: gettext('Ok'),
                        click: function() {
                            $(this).dialog('close');
                            gallery.setItemDescription($item, $template.find('textarea').val());
                        }
                    }
                ],
                close: function() {
                    dialog.empty();
                    dialog.remove();
                    dialog = null;
                }
            });
        });

        return false;
    });

})(jQuery);
