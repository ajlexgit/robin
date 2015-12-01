(function() {

    /*
        Параллакс-эффект для блока.
        Блок должен иметь position, отличный от static.

        Требует:
            jquery.utils.js, media_intervals.js

        Параметры:
            selector        - селектор выбора элемента, который будет перемещаться
            easing          - функция сглаживания перемещения фона
            extraHeight     - добавление высоты к перемещающемуся элементу в процентах
            minEnabledWidth - минимальная ширина экрана, при которой элемент перемещается

        Пример:
            <div id="block">
                <img class="parallax" src="/img/bg.jpg">
                ...
            </div>

            $(document).ready(function() {
                Parallax.create('#block');

                // или

                $('#block').parallax();
            });
     */

    var $window = $(window);
    var parallaxes = [];

    window.Parallax = Class(null, function(cls, superclass) {
        cls.init = function(block, options) {
            this.$block = $(block).first();
            if (!this.$block.length) {
                console.error('Parallax: block not found');
                return false;
            }

            // настройки
            this.opts = $.extend({
                selector: '.parallax',
                easing: 'easeInOutQuad',
                extraHeight: 50,
                minEnabledWidth: 768
            }, options);

            // передвигающийся элемент
            this.$bg = this.$block.find(this.opts.selector);
            if (!this.$bg.length) {
                console.error('Parallax: background not found');
                return false;
            }

            // отвязывание старого экземпляра
            var old_instance = this.$block.data(cls.dataParamName);
            if (old_instance) {
                old_instance.destroy();
            }

            this.$block.css({
                overflow: 'hidden'
            });

            // интервал ширины окна, на котором модуль включен
            var that = this;
            this._media_interval = MediaInterval.create(this.opts.minEnabledWidth, 0);
            this._media_interval.enter(function() {
                that.enable()
            }).leave(function() {
                that.disable()
            });

            // включаем, если интервал активен
            if (this._media_interval.is_active()) {
                this.enable();
            }

            // показ параллакса, после того, как он спозиционирован
            this.$bg.show();

            // Сохраняем объект в массив для использования в событиях
            parallaxes.push(this);

            this.$block.data(cls.dataParamName, this);
        };

        /*
            Отвязывание плагина
         */
        cls.prototype.destroy = function() {
            this.disable();
            this._media_interval.destroy();
            this.$block.removeData(cls.dataParamName);

            var index = parallaxes.indexOf(this);
            if (index >= 0) {
                parallaxes.splice(index, 1);
            }
        };

        /*
            Включение параллакса
         */
        cls.prototype.enable = function() {
            if (this._enabled) {
                return
            } else{
                this._enabled = true;
            }

            this.$bg.css({
                minHeight: (100 + this.opts.extraHeight) + '%'
            });

            this.process();
        };

        /*
            Отключение параллакса
         */
        cls.prototype.disable = function() {
            if (!this._enabled) {
                return
            } else {
                this._enabled = false;
            }

            this.$bg.css({
                minHeight: '100%',
                top: ''
            });
        };

        /*
            Расчет смещения картинки по текущему положению окна
         */
        cls.prototype.process = function(win_scroll, win_height) {
            if (!this._enabled) {
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

            var eProgress = $.easing[this.opts.easing](scrollPosition);
            var backgroundOffset = eProgress * this.opts.extraHeight;

            this.$bg.css({
                top: -backgroundOffset + '%'
            });
        };
    });
    Parallax.dataParamName = 'parallax';


    var applyParallaxes = function() {
        var win_scroll = $window.scrollTop();
        var win_height = $window.height();

        $.each(parallaxes, function(i, item) {
            $.animation_frame(function() {
                item.process(win_scroll, win_height);
            })(item.$bg.get(0));
        });
    };

    $window.on('scroll.parallax', applyParallaxes);
    $window.on('load.parallax', applyParallaxes);

    $.fn.parallax = function(options) {
        return this.each(function() {
            Parallax.create(this, options);
        })
    }

})(jQuery);
