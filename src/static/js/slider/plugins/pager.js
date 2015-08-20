(function($) {

    window.PagerPlugin = (function(parent) {
        var defaults = {
            pagerClass: 'slider-pager',
            itemClass: 'slider-pager-item',
            activeItemClass: 'active',
            container: null
        };

        // Инициализация плагина
        var PagerPlugin = function(settings) {
            this.opts = $.extend(true, defaults, settings);
        };

        var _ = function() { this.constructor = PagerPlugin; };
        _.prototype = parent.prototype;
        PagerPlugin.prototype = new _;


        /*
            Создание кнопок при подключении плагина
         */
        PagerPlugin.prototype.onAttach = function(slider) {
            this.createPager(slider);
        };

        /*
            Установка активной кнопки перед переходом к слайду
         */
        PagerPlugin.prototype.beforeSlide = function(slider, $toSlide, instantly) {
            this.activatePagerItemBySlide(slider, $toSlide);
        };

        /*
            Обновление кнопок при изменении кол-ва элементов в слайде
         */
        PagerPlugin.prototype.afterSetSlideItems = function(slider) {
            this.createPager(slider);
        };


        /*
            Создание кнопок
         */
        PagerPlugin.prototype.createPager = function(slider) {
            this.$container = this.getContainer(slider);
            if (this.$container.length) {
                this.$container = this.$container.first();
                this.createPagerItems(slider);
                this.activatePagerItemBySlide(slider, slider.$currentSlide);
            } else {
                this.$container = null;
            }
        };

        /*
            Возвращает контейнер, в который будут добавлены кнопки
         */
        PagerPlugin.prototype.getContainer = function(slider) {
            if (this.opts.container) {
                var $container = $(this.opts.container);
            } else {
                $container = slider.$root
            }
            return $container;
        };

        /*
            Добавление кнопок в DOM
         */
        PagerPlugin.prototype.createPagerItems = function(slider) {
            this.$container.find('.' + this.opts.pagerClass).remove();
            var $wrapper = $('<div/>').addClass(this.opts.pagerClass);
            this.$container.append($wrapper);

            for(var i=0;i<slider.$slides.length;i++) {
                var $item = $('<a>').addClass(this.opts.itemClass)
                    .data('slideIndex', i)
                    .text(i+1);
                $wrapper.append($item);
            }

            $wrapper.on('click.slider', '.' + this.opts.itemClass, function() {
                var $self = $(this);
                var slideIndex = $self.data('slideIndex') || 0;
                slider.slideTo(slider.$slides.eq(slideIndex));
            });
        };

        /*
            Активация соответствующей кнопки по объекту слайда
         */
        PagerPlugin.prototype.activatePagerItemBySlide = function(slider, $slide) {
            var slideIndex = slider.$slides.index($slide);
            if (this.$container.length) {
                var $item = this.$container.find('.' + this.opts.itemClass).eq(slideIndex);
                $item.addClass(this.opts.activeItemClass);
                $item.siblings('.' + this.opts.itemClass + '.' + this.opts.activeItemClass)
                    .removeClass(this.opts.activeItemClass);
            }
        };

        return PagerPlugin;
    })(SliderPlugin);

})(jQuery);
