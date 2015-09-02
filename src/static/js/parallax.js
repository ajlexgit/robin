(function() {

    /*
        Параллакс-эффект для блока.
        Блок должен иметь position, отличный от static.

        Требует:
            jquery.utils.js

        Пример:
            <div id="block">
                <div class="parallax" style="background-image: url(../img/bg.jpg)"></div>
                ...
            </div>

            $(document).ready(function() {
                new Parallax('#block');
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

            this.$bg = this.$block.find(this.opts.backgroundSelector);
            if (!this.$bg.length) {
                console.error('Parallax can\'t find background');
                return
            }

            // включение
            this.enable();

            // Сохраняем объект в массив для использования в событиях
            parallaxes.push(this);
        };

        Parallax.prototype.getDefaultOpts = function() {
            return {
                backgroundSelector: '.parallax',
                backgroundExtraHeight: 100,
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

            this.$block.css({
                overflow: 'hidden'
            });
            this.$bg.css({
                height: (100 + this.opts.backgroundExtraHeight) + '%'
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

            this.$block.css({
                overflow: ''
            });
            this.$bg.css({
                height: '100%',
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
            
            var backgroundOffset = scrollPosition * this.opts.backgroundExtraHeight;
            this.$bg.css({
                top: -this.opts.backgroundExtraHeight + backgroundOffset + '%'
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

})(jQuery);
