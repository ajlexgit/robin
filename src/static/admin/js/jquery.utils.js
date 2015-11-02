(function($) {

    // ======================================================================================
    //      ANIMATION MAGIC
    // ======================================================================================

    var emptyHandler = $.noop;
    if (document.addEventListener) {
        if ('onwheel' in document) {
            // IE9+, FF17+, Ch31+
            document.addEventListener("wheel", emptyHandler);
        } else if ('onmousewheel' in document) {
            // устаревший вариант события
            document.addEventListener("mousewheel", emptyHandler);
        } else {
            // Firefox < 17
            document.addEventListener("MozMousePixelScroll", emptyHandler);
        }
    } else {
        // IE8-
        document.attachEvent("onmousewheel", emptyHandler);
    }

    // ======================================================================================
    //      ANIMATION UTILS
    // ======================================================================================

    var handler = window.requestAnimationFrame ||
        window.webkitRequestAnimationFrame ||
        window.mozRequestAnimationFrame ||
        window.oRequestAnimationFrame ||
        window.msRequestAnimationFrame ||
        function(callback) {
            window.setTimeout(callback, 1000 / 60);
        };

    /*
        Обертка requestAnimationFrame для функций, работающих с CSS-анимацией.
     */
    $.animation_frame = function(callback, element) {
        return $.proxy(handler, window, callback, element)
    };


    /*
        Кастомная JS-анимация. Главным образом предназначена для
        анимации CSS3-свойств, которые не поддерживаются jQuery.

        Есть возможность поставить анимацию на паузу.

        Параметры:
            duration: 1000                          - длительность анимации
            delay: 20                               - частота фреймов анимации
            easing: 'linear'                        - функция сглаживания
            paused: false                           - создать приостановленной

            init: $.noop                            - callback инициализации
            step: function(eProgress)               - шаг анимации
            start: $.noop                           - callback запуска анимации
            stop: $.noop                            - callback остановки анимации
            complete: $.noop                        - callback полного завершения анимации

        Методы:
            start()     - запуск анимации
            stop()      - приостановить анимацию
     */
    var Animation = (function() {
        var Animation = function(settings) {
            this.opts = $.extend({
                duration: 1000,
                delay: 20,
                easing: 'linear',
                paused: false,

                init: $.noop,
                step: $.noop,
                start: $.noop,
                stop: $.noop,
                complete: $.noop
            }, settings);

            this._progress = 0;
            this._paused = true;
            this._duration = Math.max(this.opts.duration || 0, 20);
            this._deferred = $.Deferred();
            this._deferred.promise(this);

            this.opts.init.call(this);

            if (!this.opts.paused) {
                this.start();
            }
        };


        // Запуск анимации
        Animation.prototype.start = function() {
            if (this._paused && (this._progress < 1)) {
                this._paused = false;

                if (this._progress) {
                    this._startTime = $.now() - (this._progress * this._duration);
                } else {
                    this._startTime = $.now();
                }

                var timerHandle = $.proxy(this._timerHandle, this);
                this._timer = setInterval(timerHandle, this.opts.delay);

                this.opts.start.call(this);
            }
            return this
        };

        // Остановка анимации
        Animation.prototype.stop = function(jumpToEnd) {
            if (!this._paused) {
                this._paused = true;
                clearInterval(this._timer);

                if (jumpToEnd) {
                    this._progress = 1;
                    this._applyProgress();
                    this.opts.complete.call(this);
                    this._deferred.resolve();
                } else {
                    this.opts.stop.call(this);
                }
            }
            return this
        };

        // Shortcut для инициализации изменения свойства
        Animation.prototype.autoInit = function(name, from, to) {
            this._info = this._info || {};

            this._info[name] = {
                from: from,
                diff: to - from
            }
        };

        // Shortcut для расчета нового значения свойства
        Animation.prototype.autoCalc = function(name, eProgress) {
            var info = this._info && this._info[name];
            if (!info) {
                return null
            }

            return info.from + info.diff * eProgress;
        };

        // Применение шага анимации с вычислением that._progress
        Animation.prototype._timerHandle = function() {
            if (this._paused) {
                return
            }

            this._progress = ($.now() - this._startTime) / this._duration;
            if (this._progress >= 1) {
                this.stop(true);
            } else {
                this._applyProgress();
            }
        };

        // Применение шага анимации (для уже установленного that._progress)
        Animation.prototype._applyProgress = function() {
            var easeProgress = $.easing[this.opts.easing](this._progress);
            this.opts.step.call(this, easeProgress);
        };

        return Animation;
    })();

    $.animate = function(options) {
        return new Animation(options);
    };

    // ======================================================================================
    //      ARRAY UTILS
    // ======================================================================================

    /*
        Поиск по массиву (или селектору jQuery), возвращающий
        первый результат функции handler, отличный от undefined.
     */
    $.arrayFind = function(arr, handler) {
        var i, l, result;
        for (i = 0, l = arr.length; i<l; i++) {
            result = handler.call(arr[i], arr[i]);
            if (result != undefined) {
                return result
            }
        }
    };

    // ======================================================================================
    //      EVENT UTILS
    // ======================================================================================

    /*
        Обертка над функцией, гарантирующая, что функция будет выполняется не чаще,
        чем раз в time миллисекунд.
     */
    $.rared = function(callback, time) {
        var sleeping, sleeping_call, that, args;
        return function() {
            if (sleeping) {
                sleeping_call = true;
                that = this;
                args = arguments;
                return;
            }

            callback.apply(this, arguments);
            sleeping = setTimeout(function() {
                if (sleeping_call) {
                    callback.apply(that, args);
                    sleeping_call = false;
                }
                sleeping = null;
            }, time);
        }
    };

    // ======================================================================================
    //      DOM UTILS
    // ======================================================================================

    /*
        Ищет первый DOM-элемент, соответствуюее параметрам.
        Возвращает jQuery-объект с этим элементом

        expression может быть:
            1) строковый селектор
            2) DOM-элемент или массив DOM-элементов
            3) jQuery-объект
            4) функция, возвращающая jQuery-объект
     */
    $.findFirstElement = function(expression, context) {
        if (typeof expression == 'string') {
            // string
            return $(expression, context).first();
        } else if (typeof expression == 'function') {
            // function
            var $result = expression(context);
            return $result.first();
        } else if (expression == null) {
            // null or undefined
            return $()
        } else if (expression.jquery) {
            // jQuery
            return expression.first();
        } else {
            // DOM element or array
            return $(expression).first();
        }
    };

    /*
        Обмен двух DOM-элементов местами
     */
    $.swapElements = function(elm1, elm2) {
        var parent1, next1,
            parent2, next2;

        parent1 = elm1.parentNode;
        next1 = elm1.nextSibling;
        parent2 = elm2.parentNode;
        next2 = elm2.nextSibling;

        parent1.insertBefore(elm2, next1);
        parent2.insertBefore(elm1, next2);
    };

    /*

        Плагин, устанавливающий высоту элемента равной высоте окна,
        при условии, что позволяет высота содержимого.

        Пример:
            $.winHeight('.block', 0.9);      - разовая установка высоты на 90% высоты окна
            $('.block').winHeight(0.9);      - обновляемая высота d 90% высоты окна

     */

    var winBlocks = [];
    var $window = $(window);

    $.winHeight = function($blocks, multiplier) {
        var win_height = document.documentElement.clientHeight;

        if ($.isFunction(multiplier)) {
            multiplier = multiplier() || 1;
        } else {
            multiplier = multiplier || 1;
        }

        if (!$blocks.jquery) {
            $blocks = $($blocks);
        }

        return $blocks.each(function() {
            var $block = $(this).height('auto');
            var block_height = $block.outerHeight();
            var final_height = Math.round(win_height * multiplier);
            $block.outerHeight(Math.max(block_height, final_height));
        })
    };

    // Обновление высот блоков при ресайзе
    $window.on('resize.winHeight', $.rared(function() {
        $.each(winBlocks, function(index, winBlock) {
            $.winHeight(winBlock.$block, winBlock.multiplier);
        });
    }, 50));

    $.fn.winHeight = function(multiplier) {
        return this.each(function() {
            var $block = $(this);

            var winBlock = {
                $block: $block,
                multiplier: multiplier
            };
            winBlocks.push(winBlock);

            $.winHeight($block, multiplier);
        });
    };


    /*
        Получение ссылки на картинку
     */
    $.getSrc = function(image_expr) {
        var $image = $.findFirstElement(image_expr);
        if (!$image.length) return;
        return $image.prop('currentSrc') || $image.prop('src');
    };

    /*
        Возвращает Deferred-объект, сигнализирубщий окончание загрузки картинки
     */
    $.imgDeferred = function(image_expr) {
        var d = $.Deferred();
        var $image = $.findFirstElement(image_expr);
        if (!$image.length) {
            console.error('$.imageDeferred can\'t find image "' + image_expr + '"');
            return d.reject($());
        }

        $image.one('load', function() {
            d.resolve($image);
        }).one('error', function() {
            d.reject($image);
        });

        if ($image.get(0).complete) {
            return d.resolve($image);
        }

        return d;
    };

})(jQuery);
