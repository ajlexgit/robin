(function($) {

    var DROPDOWN_MAX_WIDTH = 400;

    var SpriteImage = (function() {
        function SpriteImage($root) {
            this.$root = $root;
            this.$input = $root.find('input:first');
            this.$wrapper = $root.find('.wrapper');
            this.$dropdown = $root.find('.sprite-icon-dropdown');

            // Расчет Dropdown
            var $items = this.$dropdown.children();
            var $first_item = $items.eq(0);
            var item_width = $first_item.outerWidth() + parseInt($first_item.css('margin-left')) +
                parseInt($first_item.css('margin-right'));
            var hor_count = Math.min(parseInt(DROPDOWN_MAX_WIDTH / item_width), $items.length);
            this.$dropdown.width(hor_count * item_width);

            // Events
            var that = this;
            this.$root.off('.sprite-image');
            this.$root.on('click.sprite-image', '.sprite-icon-preview', function() {
                if (!that.$wrapper.hasClass('opened')) {
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
            that.$wrapper.addClass('opened');
            $(document).off('.sprite-image').on('click.sprite-image', function() {
                that.closeDropdown();
            });
        };

        SpriteImage.prototype.closeDropdown = function() {
            $(document).off('.sprite-image');
            this.$wrapper.removeClass('opened');
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