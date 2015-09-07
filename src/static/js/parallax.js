(function() {

    /*
        Параллакс-эффект для блока.
        Блок должен иметь position, отличный от static.

        Требует:
            jquery.utils.js

        Пример:
            <div id="block">
                <img class="parallax" src="/img/bg.jpg">
                ...
            </div>

            $(document).ready(function() {
                new Parallax('#block');
                // или
                $('#block').parallax();
            });
     */


    var $window = $(window);
    var parallaxes = [];

    window.Parallax = (function() {
        var Parallax = function(block, options) {
            this.$block = $.findFirstElement(block);
            if (!this.$block.length) {
                console.error('Parallax can\'t find block');
                return
            }

            // настройки
            this.opts = $.extend(true, this.getDefaultOpts(), options);

            this.$block.css({
                overflow: 'hidden'
            });

            this.$bg = this.$block.find(this.opts.selector);
            if (!this.$bg.length) {
                console.error('Parallax can\'t find background');
                return
            }

            // включение
            if (window.innerWidth >= this.opts.minEnableWidth) {
                this.enable()
            }

            // Сохраняем объект в массив для использования в событиях
            parallaxes.push(this);
        };

        Parallax.prototype.getDefaultOpts = function() {
            return {
                selector: '.parallax',
                extraHeight: 75,
                minEnableWidth: 768
            }
        };

        /*
            Включение параллакса
         */
        Parallax.prototype.enable = function() {
            if (this.enabled) {
                return
            } else{
                this.enabled = true;
            }

            this.$bg.css({
                minHeight: (100 + this.opts.extraHeight) + '%'
            });

            this.process();
        };

        /*
            Отключение параллакса
         */
        Parallax.prototype.disable = function() {
            if (!this.enabled) {
                return
            } else {
                this.enabled = false;
            }

            this.$bg.css({
                minHeight: '100%',
                top: ''
            });
        };

        /*
            Расчет смещения картинки по текущему положению окна
         */
        Parallax.prototype.process = function(win_scroll, win_height) {
            if (!this.enabled) {
                return
            }

            win_scroll = win_scroll || $window.scrollTop();
            win_height = win_height || $window.height();

            var block_top = this.$block.offset().top;
            var block_height = this.$block.outerHeight();
            var scrollFrom = block_top - win_height;
            var scrollTo = block_top + block_height;
            if ((win_scroll < scrollFrom) || (win_scroll > scrollTo)) {
                return
            }

            var scrollLength = scrollTo - scrollFrom;
            var scrollPosition = (win_scroll - scrollFrom) / scrollLength;

            var backgroundOffset = scrollPosition * this.opts.extraHeight;
            this.$bg.css({
                top: -this.opts.extraHeight + backgroundOffset + '%'
            });
        };

        return Parallax;
    })();


    var applyParallaxes = function() {
        var win_scroll = $window.scrollTop();
        var win_height = $window.height();

        $.each(parallaxes, function(i, obj) {
            $.animation_frame(function() {
                obj.process(win_scroll, win_height);
            })(obj.$bg.get(0));
        });
    };

    $window.on('scroll.parallax', applyParallaxes);
    $window.on('load.parallax', applyParallaxes);
    $window.on('resize.parallax', $.rared(function() {
        $.each(parallaxes, function() {
            if (window.innerWidth < this.opts.minEnableWidth) {
                this.disable()
            } else {
                this.enable()
            }
        });
    }, 100));

    $.fn.parallax = function(options) {
        this.each(function() {
            new Parallax(this, options);
        })
    }

})(jQuery);
