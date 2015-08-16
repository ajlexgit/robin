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

            // оборачиваем список в обертку
            this.$root = this.createRoot($element);

            // сохраняем массив items
            this.$items = this.getItems();

            // создаем слайды
            this.createSlides(this.opts.slideItems);
        };

        // Метод, возвращающий объект настроек по умолчанию
        Slider.prototype.getDefaultOpts = function() {
            return {
                rootClass: 'slider-root',
                listClass: 'slider-list',
                slideClass: 'slider-slide',
                itemSelector: 'img',
                slideItems: 2
            };
        };

        // Метод, возвращающий ссылку на объект-список
        Slider.prototype.createList = function($element) {
            return $element.addClass(this.opts.listClass);
        };

        // Метод, возвращающий ссылку на объект-обертку
        Slider.prototype.createRoot = function($element) {
            var $root = $('<div>').addClass(this.opts.rootClass);
            $element.wrap($root);
            return $root;
        };

        // Метод, возвращающий массив ссылок на items
        Slider.prototype.getItems = function() {
            var $items = this.$list.find(this.opts.itemSelector);
            return $items.toArray();
        };

        // Метод, возвращающий массив ссылок на items
        Slider.prototype.createSlides = function(slideItems) {
            this.$list.empty();
            var slide_count = Math.ceil(this.$items.length / slideItems);
            for (var i=0;i<slide_count;i++) {
                var $slide = $('<div>').addClass(this.opts.slideClass);
                $slide.append(this.$items.slice(i * slideItems, (i+1) * slideItems));
                this.$list.append($slide);
            }
        };

        return Slider;
    })();

})(jQuery);
