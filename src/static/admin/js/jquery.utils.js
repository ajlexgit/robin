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

    // ======================================================================================
    //      CANVAS UTILS
    // ======================================================================================

    /*
        Возвращает размеры canvas с учетом ограничений браузера.
        Параметры:
            img_width, img_height - исходные размеры картинки
            max_width, max_height - целевые ограничения
    */
    window.canvasSize = function(img_width, img_height, max_width, max_height) {
        var ratio = img_width / img_height;
        var width, height;

        // Размеры с учетом max_width/max_height
        if (!max_width) {
            if (max_height) {
                // max_width == 0
                height = Math.min(img_height, max_height);
                width = Math.round(height * ratio);
            } else {
                // max_width == 0 && max_height == 0
                width = img_width;
                height = img_height;
            }
        } else if (!height) {
            // max_height == 0
            width = Math.min(img_width, max_width);
            height = Math.round(width / ratio);
        }

        // Ограничение IE
        if (width > 4096) {
            width = 4096;
            height = Math.round(width / ratio);
        }
        if (height > 4096) {
            height = 4096;
            width = Math.round(height * ratio);
        }

        // Ограничение iOS
        if (width * height > 5000000) {
            width = Math.floor(Math.sqrt(5000000 * ratio));
            height = Math.floor(5000000 / Math.sqrt(5000000 * ratio));
        }

        return {
            width: width,
            height: height
        };
    };


    /*
        Создает Deferred-объект, который загружает картинку из файла.
    */
    $.fileReaderDeferred = function(file) {
        var df = $.Deferred();
        if (!window.FileReader) {
            return df.reject('FileReader not supported');
        }
        if (file instanceof Blob == false) {
            return df.reject('Not a file');
        }

        var reader = new FileReader();
        reader.onload = function(event) {
            df.resolve(event.target.result);
        };
        reader.onerror = function() {
            df.reject('can not read');
        };
        reader.readAsDataURL(file);
        return df.promise();
    };


    /*
        Создает Deferred-объект, который читает файл по URL.
     */
    $.urlReader = function(url) {
        var df = $.Deferred();

        var xhr = new XMLHttpRequest();
        xhr.open('GET', url, true);

        // Hack to pass bytes through unprocessed.
        xhr.overrideMimeType('text/plain; charset=x-user-defined');

        xhr.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                df.resolve(this.responseText);
            }
        };
        xhr.onerror = function() {
            df.reject('can not read');
        };
        xhr.send();
        return df.promise();
    };


    /*
        Создает Deferred-объект, который загружает картинку.
    */
    $.loadImageDeferred = function(src) {
        var df = $.Deferred();
        var img = new Image();
        img.onload = function() {
            df.resolve(this);
        };
        img.onerror = function() {
            df.reject('Not image');
        };
        img.src = src;
        return df.promise();
    };


    /*
        Возвращает canvas с картинкой с указанными ограничениями размеров.
        Можно не указывать размеры, или указать один из них.

        Уменьшение размера происходит очень быстро, но некачественно.

        Пример:
            $.fileReaderDeferred($('#test').prop('files').item(0)).done(function(src) {
                $.loadImageDeferred(src).done(function(img) {
                    var canvas = $.imageToCanvas(img, 360, 360);
                    $('#test').after(canvas);
                });
            });
    */
    $.imageToCanvas = function(source, max_width, max_height) {
        // Первое уменьшение до максимально возможного размера
        var canvas = document.createElement("canvas");
        $.extend(canvas, canvasSize(
            source.width, source.height, max_width, max_height
        ));
        var context = canvas.getContext && canvas.getContext('2d');
        if (!context) {
            console.error('Canvas not supported');
            return
        }
        context.drawImage(source, 0, 0, canvas.width, canvas.height);
        return canvas;
    };


    /*
        Возвращает Deferred-объект, который возвращает canvas с картинкой с
        указанными ограничениями размеров.
        Можно не указывать размеры, или указать один из них.

        Качество выше, чем у $.imageToCanvas, но всё равно не идеально.
        Для лучшего качества используете плагин pica: https://github.com/nodeca/pica

        Пример:
            $.fileReaderDeferred($('#test').prop('files').item(0)).done(function(src) {
                $.loadImageDeferred(src).done(function(img) {
                    $.imageToCanvasDeferred(img, 360, 360).done(function(canvas) {
                        $('#test').after(canvas);
                    });
                });
            });
    */
    $.imageToCanvasDeferred = function(source, max_width, max_height) {
        var df = $.Deferred();

        // Первое уменьшение. Максимальный размер
        var canvas = $.imageToCanvas(source);
        var source_size = {
            width: canvas.width,
            height: canvas.height
        };


        var context = canvas.getContext('2d');
        var target_size = canvasSize(canvas.width, canvas.height, max_width, max_height);
        var step_func = function(dim) {
            return Math.round(dim * 0.5);
        };

        // Последовательное уменьшение canvas
        var run;
        (run = function() {
            if (source_size.width <= target_size.width) {
                return df.resolve(canvas);
            }

            setTimeout(function() {

                if (step_func(source_size.width) <= target_size.width) {
                    // Последний шаг
                    var temp_canvas = document.createElement("canvas");
                    temp_canvas.width = target_size.width;
                    temp_canvas.height = target_size.height;
                    temp_canvas.getContext('2d').drawImage(canvas,
                        0, 0, source_size.width, source_size.height,
                        0, 0, temp_canvas.width, temp_canvas.height
                    );

                    canvas.src = 'about:blank';
                    canvas.width = 1;
                    canvas.height = 1;

                    canvas = temp_canvas;
                    source_size = target_size;
                } else {
                    context.drawImage(canvas,
                        0, 0, source_size.width, source_size.height,
                        0, 0, step_func(source_size.width), step_func(source_size.height));
                    source_size.width = step_func(source_size.width);
                    source_size.height = step_func(source_size.height);
                }

                run();
            }, 0);
        })();

        return df.promise();
    };


    /*
        Создание превью по параметрам.

        Параметры:
            source      - Image-объект или canvas
            width       - целевая ширина
            height      - целевая высота
            crop        - можно ли обрезать картинку
            stretch     - можно ли растягивать картинку
            max_width   -
            max_height  -
            coords      - кординаты обрезки исходной картинки
            offset      - относительное смещение картинки относительно холста
            center      - относительные координаты центра накладываемой картинки
            background  - цвет фона холста
     */
    $.previewCanvas = function(options) {
        var settings = $.extend({
            source: null,
            width: 100,
            height: 100,
            crop: true,
            stretch: false,
            max_width: 0,
            max_height: 0,
            coords: null,
            offset: [0.5, 0.5],
            background: [255, 255, 255, 0]
        }, options);

        if (!settings.coords) {
            settings.coords = [0, 0, settings.source.width, settings.source.height];
        }
        var coords_ratio = settings.coords[2] / settings.coords[3];

        if (!settings.offset) {
            settings.offset = [0.5, 0.5];
        }

        if (!settings.background) {
            settings.background = [255, 255, 255, 0];
        }
        settings.background[3] = (settings.background[3] / 256).toFixed(2);

        var target_size = [settings.width, settings.height];
        var final_w, final_h, final_l = 0, final_t = 0;

        var canvas = document.createElement("canvas");
        var context = canvas.getContext && canvas.getContext('2d');
        if (!context) {
            console.error('Canvas not supported');
            return
        }

        if (settings.crop) {
            // --- можно обрезать ---
            if (settings.stretch) {
                // можно растягивать
            } else {
                // нельзя растягивать
                target_size[0] = Math.min(target_size[0], settings.coords[2]);
                target_size[1] = Math.min(target_size[1], settings.coords[3]);
            }

            // Задаем размер канвы
            $.extend(canvas, canvasSize(target_size[0], target_size[1]));

            if ((target_size[0] == settings.coords[2]) && (target_size[1] == settings.coords[3])) {
                // Если целевой размер больше - оставляем картинку без изменений
                final_w = target_size[0];
                final_h = target_size[1];
            } else {
                var target_ratio = target_size[0] / target_size[1];
                if (coords_ratio >= target_ratio) {
                    // картинка более "широкая", чем надо
                    final_h = target_size[1];
                    final_w = final_h * coords_ratio;
                    final_l = (target_size[0] - final_w) / 2;

                    final_w = Math.round(final_w);
                    final_l = Math.round(final_l);
                } else {
                    // картинка более "высокая", чем надо
                    final_w = target_size[0];
                    final_h = final_w / coords_ratio;
                    final_t = (target_size[1] - final_h) / 2;

                    final_h = Math.round(final_h);
                    final_t = Math.round(final_t);
                }
            }
        } else {
            // --- нельзя обрезать ---

            var image_size = [
                Math.min(settings.max_width || target_size[0], target_size[0] || settings.max_width),
                Math.min(settings.max_height || target_size[1], target_size[1] || settings.max_height)
            ];

            // обработка случаев, когда size содержит нули, но заданы max_width/max_height
            target_size[0] = target_size[0] || image_size[0];
            target_size[1] = target_size[1] || image_size[1];

            // нули и в max_width и в size
            if (target_size[0] == 0) {
                var new_w = target_size[1] * coords_ratio;

                if (!settings.stretch) {
                    new_w = Math.min(new_w, settings.coords[2])
                }

                target_size[0] = image_size[0] = Math.floor(new_w);
            } else if (target_size[1] == 0) {
                var new_h = target_size[0] / coords_ratio;

                if (!settings.stretch) {
                    new_h = Math.min(new_h, settings.coords[3])
                }

                target_size[1] = image_size[1] = Math.floor(new_h);
            }

            // Новый размер канвы
            $.extend(canvas, canvasSize(target_size[0], target_size[1]));

            // заполняем канву цветом
            context.fillStyle = 'rgba(' + settings.background.join(',') + ')';
            context.fillRect(0, 0, canvas.width, canvas.height);

            if (settings.stretch) {
                // можно растягивать
                var image_ratio = image_size[0] / target_size[1];
                if (coords_ratio >= image_ratio) {
                    // картинка более "широкая", чем надо
                    final_w = image_size[0];
                    final_h = final_w / coords_ratio;
                } else {
                    // картинка более "высокая", чем надо
                    final_h = image_size[1];
                    final_w = final_h * coords_ratio;
                }
            } else {
                // нельзя растягивать
                final_w = settings.coords[2];
                final_h = settings.coords[3];
                if (final_w > image_size[0]) {
                    final_w = image_size[0];
                    final_h = final_w / coords_ratio;
                }
                if (final_h > image_size[1]) {
                    final_h = image_size[1];
                    final_w = final_h * coords_ratio;
                }
            }

            if (settings.center && (settings.center.length == 2)) {
                final_l = Math.max(0, target_size[0] * settings.center[0] - final_w / 2);
                final_t = Math.max(0, target_size[1] * settings.center[1] - final_h / 2);
            } else {
                final_l = (target_size[0] - final_w) * settings.offset[0];
                final_t = (target_size[1] - final_h) * settings.offset[1];
            }
        }

        context.drawImage(
            settings.source,
            settings.coords[0],
            settings.coords[1],
            settings.coords[2],
            settings.coords[3],
            final_l,
            final_t,
            final_w,
            final_h
        );

        return canvas;
    };

})(jQuery);