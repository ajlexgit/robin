(function() {

    /*
        Параллакс-эффект для блока.
        Блок должен иметь position, отличный от static.

        Требует:
            jquery.utils.js

        Параметры:
            selector        - селектор выбора элемента, который будет перемещаться
            easing          - функция сглаживания перемещения фона
            extraHeight     - добавление высоты к перемещающемуся элементу в процентах
            minEnableWidth  - минимальная ширина экрана, при которой элемент перемещается

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
                console.error('Parallax can\'t find block');
                return false;
            } else {
                // отвязывание старого экземпляра
                var old_instance = this.$block.data(Parallax.dataParamName);
                if (old_instance) {
                    old_instance.destroy();
                }
                this.$block.data(Parallax.dataParamName, this);
            }

            // настройки
            this.opts = $.extend({
                selector: '.parallax',
                easing: 'easeInOutQuad',
                extraHeight: 50,
                minEnableWidth: 768
            }, options);

            this.$block.css({
                overflow: 'hidden'
            });

            // передвигающийся элемент
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

        /*
            Отвязывание плагина
         */
        cls.prototype.destroy = function() {
            this.disable();
            this.$block.removeData(Parallax.dataParamName);

            var index = parallaxes.indexOf(this);
            if (index >= 0) {
                parallaxes.splice(index, 1);
            }
        };

        /*
            Включение параллакса
         */
        cls.prototype.enable = function() {
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
        cls.prototype.disable = function() {
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
        cls.prototype.process = function(win_scroll, win_height) {
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
        return this.each(function() {
            Parallax.create(this, options);
        })
    }

})(jQuery);
