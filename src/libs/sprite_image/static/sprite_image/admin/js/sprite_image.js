(function($) {

    var SpriteImage = Class(null, function SpriteImage(cls, superclass) {
        cls.dataParamName = 'sprite_image';


        cls.init = function(root) {
            this.$root = $(root).first();
            if (!this.$root.length) {
                return this.raise('root element not found');
            }

            this.$input = this.$root.find('input:first');
            if (!this.$input.length) {
                return this.raise('input element not found');
            }

            this.$dropdown = this.$root.find('.sprite-icon-dropdown');
            if (!this.$dropdown.length) {
                return this.raise('dropdown block not found');
            }

            this.$preview = this.$root.find('.sprite-icon-preview');
            if (!this.$preview.length) {
                return this.raise('preview not found');
            }

            // отвязывание старого экземпляра
            var old_instance = this.$root.data(this.dataParamName);
            if (old_instance) {
                old_instance.destroy();
            }

            // Events
            var that = this;
            this.$root.on('click.sprite-image', '.sprite-icon-preview', function() {
                if (!that.$root.hasClass('opened')) {
                    that.openDropdown();
                    return false;
                }
            }).on('click.sprite-image', '.sprite-icon-item', function() {
                that.selectItem($(this));
                that.closeDropdown(true);
            });

            this.$root.data(this.dataParamName, this);
        };

        /*
            Освобождение ресурсов
         */
        cls.destroy = function() {
            this.$root.off('.sprite-image');
            this.$root.removeData(this.dataParamName);
        };

        /*
            Выбор элемента списка
         */
        cls.selectItem = function($item) {
            $item.addClass('active').siblings('.active').removeClass('active');
            this.$preview.css({
                backgroundPosition: $item.css('background-position')
            });
            this.$input.val($item.data('key'));
        };

        /*
            Открытие выпадающего списка
         */
        cls.openDropdown = function() {
            this.$root.addClass('opened');
            var margin = parseInt(this.$preview.width()) + 18;
            this.$dropdown.css('margin-left', margin).stop().slideDown(200);

            var that = this;
            $(document).one('click.sprite-image', function(event) {
                var $target = $(event.target);
                if (!$target.closest(that.$dropdown.children('.sprite-icon-list')).length) {
                    that.closeDropdown();
                }
            });
        };

        /*
            Закрытие выпадающего списка
         */
        cls.closeDropdown = function(instant) {
            this.$root.removeClass('opened');

            if (instant) {
                this.$dropdown.stop().hide();
            } else {
                this.$dropdown.stop().slideUp(200, function() {
                    $(this).removeAttr('style')
                });
            }
        };
    });


    $(document).ready(function() {
        $('.sprite-icon-field').each(function() {
            if (!$(this).closest('.empty-form').length) {
                SpriteImage(this);
            }
        });

        if (window.Suit) {
            Suit.after_inline.register('sprite-icon', function(inline_prefix, row) {
                row.find('.sprite-icon-field').each(function() {
                    SpriteImage(this);
                });
            });
        }
    });

})(jQuery);