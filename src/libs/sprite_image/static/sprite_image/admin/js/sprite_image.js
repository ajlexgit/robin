(function($) {

    var SpriteImage = (function() {
        function SpriteImage($root) {
            this.$root = $root;
            this.$input = $root.find('input:first');
            this.$dropdown = $root.find('.sprite-icon-dropdown');

            // Events
            var that = this;
            this.$root.off('.sprite-image');
            this.$root.on('click.sprite-image', '.sprite-icon-preview', function() {
                if (!that.$root.hasClass('opened')) {
                    that.openDropdown();
                    return false;
                }
            }).on('click.sprite-image', '.sprite-icon-item', function() {
                that.selectItem($(this));
            });
        }

        SpriteImage.prototype.selectItem = function($item) {
            $item.addClass('active').siblings('.active').removeClass('active');
            this.$root.find('.sprite-icon-preview').css({
                backgroundPosition: $item.css('background-position')
            });
            this.$input.val($item.data('key'));
        };

        // Dropdown
        SpriteImage.prototype.openDropdown = function() {
            var that = this;
            that.$root.addClass('opened');
            that.$dropdown.stop().slideDown(300);
            $(document).off('.sprite-image').on('click.sprite-image', function() {
                that.closeDropdown();
            });
        };

        SpriteImage.prototype.closeDropdown = function() {
            $(document).off('.sprite-image');
            this.$root.removeClass('opened');
            this.$dropdown.stop().slideUp(300, function() {
                $(this).removeAttr('style')
            });
        };

        return SpriteImage;
    })();

    $(document).ready(function() {
        $('.sprite-icon-field').each(function() {
            var self = $(this);
            if (!self.closest('.empty-form').length) {
                self.data('object', new SpriteImage(self));
            }
        });

        if (window.Suit) {
            Suit.after_inline.register('sprite-icon', function(inline_prefix, row) {
                var self = row.find('.sprite-icon-field');
                self.data('object', new SpriteImage(self));
            });
        }
    });

})(jQuery);