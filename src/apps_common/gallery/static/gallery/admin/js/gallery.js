(function($) {

    $(document).ready(function() {
        $('.gallery-standart').each(function() {
            if (!$(this).closest('.empty-form').length) {
                DefaultGallery(this);
            }
        });

        if (window.Suit) {
            Suit.after_inline.register('gallery', function(inline_prefix, row) {
                $(row).find('.gallery-standart').each(function() {
                    DefaultGallery(this);
                });
            });
        }
    }).on('click.gallery', '.create-gallery', function() {
        var $button = $(this);
        var gallery = $button.closest('.gallery').data(Gallery.prototype.DATA_KEY);
        if (!gallery) {
            console.error('Gallery object not found');
            return false;
        }

        $button.prop('disabled', true);
        gallery.createGallery().always(function() {
            $button.prop('disabled', false);
        });

        return false;
    }).on('click.gallery', '.delete-gallery', function() {
        var $button = $(this);
        var gallery = $button.closest('.gallery').data(Gallery.prototype.DATA_KEY);
        if (!gallery) {
            console.error('Gallery object not found');
            return false;
        }

        if (!confirm(gettext('Are you sure you want to delete this gallery?'))) {
            return false
        }

        $button.prop('disabled', true);
        gallery.deleteGallery().always(function() {
            $button.prop('disabled', false);
        });

        return false;
    }).on('click.gallery', '.add-gallery-video', function() {
        var $button = $(this);
        var gallery = $button.closest('.gallery').data(Gallery.prototype.DATA_KEY);
        if (!gallery) {
            console.error('Gallery object not found');
            return false;
        }

        var video_link = prompt(gettext('Paste YouTube/Vimeo video URL'), 'http://');
        if (video_link) {
            gallery.addVideo(video_link);
        }

        return false;
    }).on('click.gallery', '.item-delete', function() {
        var $button = $(this);
        var gallery = $button.closest('.gallery').data(Gallery.prototype.DATA_KEY);
        if (!gallery) {
            console.error('Gallery object not found');
            return false;
        }

        var $item = $button.closest('.gallery-item');
        gallery.deleteItem($item);

        return false;
    }).on('click.gallery', '.item-rotate-left', function() {
        var $button = $(this);
        var gallery = $button.closest('.gallery').data(Gallery.prototype.DATA_KEY);
        if (!gallery) {
            console.error('Gallery object not found');
            return false;
        }

        var $item = $button.closest('.gallery-item');
        gallery.rotateItem($item, 'left').done(function() {
            $item.find('.item-crop').removeData('crop').removeAttr('data-crop');
        });

        return false;
    }).on('click.gallery', '.item-rotate-right', function() {
        var $button = $(this);
        var gallery = $button.closest('.gallery').data(Gallery.prototype.DATA_KEY);
        if (!gallery) {
            console.error('Gallery object not found');
            return false;
        }

        var $item = $button.closest('.gallery-item');
        gallery.rotateItem($item, 'right').done(function() {
            $item.find('.item-crop').removeData('crop').removeAttr('data-crop');
        });

        return false;
    }).on('click.gallery', '.item-description', function() {
        var $button = $(this);
        var gallery = $button.closest('.gallery').data(Gallery.prototype.DATA_KEY);
        if (!gallery) {
            console.error('Gallery object not found');
            return false;
        }

        var $template = $('<div>')
            .append('<textarea>')
            .appendTo('body');

        var $item = $button.closest('.gallery-item');
        gallery.getItemDescription($item).done(function(response) {
            $template.find('textarea').val(response.description);

            $template.dialog({
                title: gettext('Set description'),
                width: 460,
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
                draggable: false,
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
                            var $this = $(this);
                            $this.dialog('close');
                            gallery.setItemDescription($item, $this.find('textarea').val());
                        }
                    }
                ],
                open: function() {
                    var $this = $(this);
                    var dialog = $this.dialog('instance');
                    var $textarea = $this.find('textarea');
                    if ($.fn.autosize) {
                        $textarea.autosize({
                            callback: function() {
                                if (dialog.widget().outerHeight() < $.winHeight()) {
                                    dialog._position();
                                }
                            }
                        });
                    }
                },
                close: function() {
                    $(this).dialog('destroy');
                    $template.remove();
                }
            });
        });

        return false;
    });

})(jQuery);
