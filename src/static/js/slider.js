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

            // активация первого слайда
            this.activateSlide(this.getStartSlide());

            // Установка стиля left слайдам
            var that = this;
            this.$slides.each(function() {
                if (this == that.$currentSlide.get(0)) {
                    $(this).css('left', 0);
                } else {
                    $(this).css('left', '100%');
                }
            });

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
                loop: true,

                speed: 500,

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

        // Метод, возвращающий начальный активный слайд
        Slider.prototype.activateSlide = function($slide) {
            this.$slides.removeClass(this.opts.slideActiveClass);
            $slide.addClass(this.opts.slideActiveClass);
            this.$currentSlide = $slide;
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
            var $left = $('<div>').addClass('arrow arrow-left').appendTo($controlsParent);
            var $right = $('<div>').addClass('arrow arrow-right').appendTo($controlsParent);

            var that = this;
            $left.on('click', function() {
                that.slideLeft();
            });
            $right.on('click', function() {
                that.slideRight();
            });

            return {
                left: $left,
                right: $right
            };
        };

        // Метод, возвращающий следующий слайд
        Slider.prototype.getNextSlide = function($slide) {
            var index = this.$slides.index($slide);
            if (++index < this.$slides.length) {
                return this.$slides.eq(index);
            }

            if (this.opts.loop) {
                return this.$slides.eq(0);
            }
        };

        // Метод, возвращающий предыдущий слайд
        Slider.prototype.getPreviousSlide = function($slide) {
            var index = this.$slides.index($slide);
            if (--index >= 0) {
                return this.$slides.eq(index);
            }

            if (this.opts.loop) {
                return this.$slides.eq(this.$slides.length - 1);
            }
        };

        // Скролл к следующему слайду
        Slider.prototype.slideRight = function() {
            var $curr = this.$currentSlide;
            if ($curr._animation) {
                return
            }

            var $next = this.getNextSlide($curr);
            if (!$next || !$next.length) {
                return
            }

            $curr._animation = $.animate({
                duration: this.opts.speed,
                init: function() {
                    this.initial = parseInt($curr.get(0).style.left);
                    this.diff = -100 - this.initial;
                },
                step: function(eProgress) {
                    $curr.css('left', this.initial + this.diff * eProgress + '%');
                },
                complete: function() {
                    $curr._animation = null;
                }
            });

            this.activateSlide($next);
            $next.css('left', '100%');

            $next._animation = $.animate({
                duration: this.opts.speed,
                init: function() {
                    this.initial = parseInt($next.get(0).style.left);
                    this.diff = -this.initial;
                },
                step: function(eProgress) {
                    $next.css('left', this.initial + this.diff * eProgress + '%');
                },
                complete: function() {
                    $next._animation = null;
                }
            });
        };

        // Скролл к предыдущему слайду
        Slider.prototype.slideLeft = function() {
            var $curr = this.$currentSlide;
            if ($curr._animation) {
                return
            }

            var $prev = this.getPreviousSlide($curr);
            if (!$prev || !$prev.length) {
                return
            }

            $curr._animation = $.animate({
                duration: this.opts.speed,
                init: function() {
                    this.initial = parseInt($curr.get(0).style.left);
                    this.diff = 100 - this.initial;
                },
                step: function(eProgress) {
                    $curr.css('left', this.initial + this.diff * eProgress + '%');
                },
                complete: function() {
                    $curr._animation = null;
                }
            });

            this.activateSlide($prev);
            $prev.css('left', '-100%');

            $prev._animation = $.animate({
                duration: this.opts.speed,
                init: function() {
                    this.initial = parseInt($prev.get(0).style.left);
                    this.diff = -this.initial;
                },
                step: function(eProgress) {
                    $prev.css('left', this.initial + this.diff * eProgress + '%');
                },
                complete: function() {
                    $prev._animation = null;
                }
            });
        };

        return Slider;
    })();

})(jQuery);
