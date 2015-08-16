(function($) {

    /*
        Основа слайдеров.

        HTML input:
            <div>
                <img>
                ...
            </div>

        HTML output:
            <div role="root">
                <ul role="list">
                    <li role="slide">
                        <img role="item">
                        <img role="item">
                        ...
                    </li>
                    ...
                </ul>
            </div>
    */

    window.Slider = (function() {
        var Slider = function($element, settings) {
            if (!$element || !$element.length) {
                return
            }

            // настройки
            var defaults = this.getDefaultOpts();
            this.opts = $.extend(true, defaults, settings);

            // сохраняем ссылку на список
            this.$list = this.createList($element);
            this.$list.addClass(this.opts.listClass);

            // оборачиваем список в обертку
            this.$root = this.createRoot($element);
            this.$root.addClass(this.opts.rootClass);

            // сохраняем массив items
            this.$items = this.createItems();
            this.$items.addClass(this.opts.itemClass);

            // создаем слайды
            this.$slides = this.createSlides(this.opts.slideItems);
            this.$slides.addClass(this.opts.slideClass);

            // активация слайдов
            this.$currentSlide = this.getStartSlide();
            this.$currentSlide.addClass(this.opts.slideActiveClass);

            // --- стрелки ---
            if (this.opts.controls) {
                var $controlsParent = this.getControlsContainer();
                if ($controlsParent.length) {
                    $controlsParent = $controlsParent.first();
                    this.controls = this.createControls($controlsParent);
                }
            }
        };

        // Метод, возвращающий объект настроек по умолчанию
        Slider.prototype.getDefaultOpts = function() {
            return {
                rootClass: 'slider-root',
                listClass: 'slider-list',
                slideClass: 'slider-slide',
                slideActiveClass: 'slider-slide-active',
                itemClass: 'slider-item',

                itemSelector: 'img',
                slideItems: 2,

                controls: true,
                controlsParent: null
            };
        };

        // Метод, возвращающий ссылку на объект-список
        Slider.prototype.createList = function($element) {
            return $element;
        };

        // Метод, возвращающий ссылку на объект-обертку
        Slider.prototype.createRoot = function($element) {
            $element.wrap('<div>');
            return $element.parent();
        };

        // Метод, возвращающий массив ссылок на items
        Slider.prototype.createItems = function() {
            return this.$list.find(this.opts.itemSelector);
        };

        // Метод, возвращающий массив ссылок на items
        Slider.prototype.createSlides = function(slideItems) {
            var $slides = $();
            var slide_count = Math.ceil(this.$items.length / slideItems);

            this.$list.empty();
            for (var i=0;i<slide_count;i++) {
                var $slide = $('<div>');
                this.$list.append(
                    $slide.append(
                        this.$items.slice(i * slideItems, (i + 1) * slideItems)
                    )
                );
                $slides.push($slide.get(0));
            }
            return $slides;
        };

        // Метод, возвращающий начальный активный слайд
        Slider.prototype.getStartSlide = function() {
            return this.$slides.first();
        };

        // Метод, возвращающий контейнер, куда будут добавлены стрелки
        Slider.prototype.getControlsContainer = function() {
            if (this.opts.controlsParent) {
                var $controlsParent = $(this.opts.controlsParent);
            } else {
                $controlsParent = this.$root
            }
            return $controlsParent;
        };

        // Метод, добавляющий стрелки
        Slider.prototype.createControls = function($controlsParent) {
            console.log($controlsParent);
            var $left = $('<div>').addClass('arrow arrow-left').appendTo($controlsParent);
            var $right = $('<div>').addClass('arrow arrow-right').appendTo($controlsParent);

            return {
                left: $left,
                right: $right
            };
        };

        return Slider;
    })();

})(jQuery);
