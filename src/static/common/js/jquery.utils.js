(function($) {

    var $window = $(window);

    // ======================================================================================
    //      Событие click для браузеров и touchend для мобилок.
    //      Создано из-зи того, что на мобилах есть пауза между
    //      реальным тапом на кнопку и вызовом события click.
    // ======================================================================================
    var isMobile = false;
    if(/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|ipad|iris|kindle|Android|Silk|lge |maemo|midp|mmp|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows (ce|phone)|xda|xiino/i.test(navigator.userAgent)
        || /1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(navigator.userAgent.substr(0,4))) {
        isMobile = true;
    }
    
    window.touchClick = (isMobile && ('ontouchend' in window)) ? 'touchend' : 'click';


    // ======================================================================================
    //      Обработчик AJAX-ошибок.
    //      Ничего не делает, если запрос был прерван (aborted).
    //      Иначе, вызывает callback с ответом сервера в виде JSON-объекта
    //      (если удалось этот объект распарсить).
    // ======================================================================================

    /*
            Пример:
                $.ajax({
                    ...
                    error: $.parseError(function(response) {
                        if (response && response.message) {
                            console.error(response.message);
                        }
                    })
                })
     */
    window.DEFAULT_AJAX_ERROR = gettext('Connection error');
    $.parseError = function(callback) {
        var final_callback = callback || function(response, status) {
            if (response && response.message) {
                alert(response.message);
            } else {
                alert(window.DEFAULT_AJAX_ERROR);
            }
        };

        return function(xhr, status) {
            // AJAX прерван - ничего не делать
            if (xhr.statusText == 'abort') {
                return
            }

            if (xhr.responseText) {
                try {
                    var response = $.parseJSON(xhr.responseText + "");
                    final_callback.call(xhr, response, status);
                } catch (err) {
                    // ответ - не JSON
                    final_callback.call(xhr, '', status);
                }
            } else {
                final_callback.call(xhr, xhr.responseText, status);
            }
        };
    };


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
    //      JS classes
    // ======================================================================================

    /*
        Система классов Javascript.

        Экземпляры можно создавать через
            > ClassName(arg1, ...)

        Либо через
            > ClassName.create(arg1, ...)

        При создании экземпляров через
            > new ClassName(arg1, ...)

        всегда будет возвращен экземпляр класса,
        но неполный (в случае ошибки инициализации).


        Пример 1:
            // создание класса Point2D, унаследованного от Object
            // с функцией инициализации и методом print().

            var Point2D = Class(null, function Point2D(cls, superclass) {
                cls.init = function(x, y) {
                    this._x = parseInt(x);
                    if (isNaN(this._x)) {
                        return this.raise('invalid X');
                    };

                    this._y = parseInt(y);
                    if (isNaN(this._y)) {
                        return this.raise('invalid Y');
                    }
                }

                cls.print = function() {
                    return this._x + ':' + this._y
                }
            });

        Пример 2:
            // создание дочернего класса Point3D, унаследованного от Point2D.
            var Point3D = Class(Point2D, function Point3D(cls, superclass) {
                cls.init = function(x, y, z) {
                    superclass.init.call(this, x, y);

                    this._z = parseInt(z);
                    if (isNaN(this._z)) {
                        return this.raise('invalid Z');
                    }
                };

                cls.print = function() {
                    return superclass.print.call(this) + ':' + this._z
                }
            });

        Пример 3:
            // создание экземпляров классов
            > Point2D(6)
            < Point2D: invalid Y
            < undefined

            > Point2D(6, 'fail')
            < Point2D: invalid Y
            < undefined

            > Point2D(6, 7)
            < Object {...}


            > Point3D('fail', 6, 7)
            < Point3D: invalid X
            < undefined

            > Point3D(6, 7)
            < Point3D: invalid Z
            < undefined

     */
    window.Class = function(parent, class_constructor) {
        if (typeof class_constructor != 'function') {
            throw Error('class-constructor function required');
        }

        // получение имени функции
        var name = class_constructor.name;
        if (name === undefined) {
            var match = /function ([^\(]+)\(/ig.exec(class_constructor.toString());
            if (match) {
                name = match[1];
            }
        }
        if (!name) {
            throw Error('class-constructor should be a named function');
        }

        // установка прототипа, унаследованного от родительского
        var ClassObj = function() {
            return ClassObj.prototype.create.apply(null, arguments);
        };
        ClassObj.prototype = Object.create(parent && parent.prototype);
        ClassObj.prototype.constructor = ClassObj;
        ClassObj.superclass = parent;
        ClassObj.prototype.__name__ = class_constructor.name;

        // конструктор экземпляров
        ClassObj.prototype.create = function() {
            var obj = Object.create(ClassObj.prototype);
            obj.constructor = ClassObj;

            try {
                obj.init.apply(obj, arguments);
                return obj;
            } catch (err) {
                if (err instanceof ClassError) {
                    obj.error(err.message);
                } else {
                    throw err;
                }
            }
        };

        // Возбуждение исключения. Имеет смысл вызывать в методе init
        ClassObj.prototype.raise = function(message) {
            throw new ClassError(message);
        };

        // Вывод ошибки в консоль
        ClassObj.prototype.error = function() {
            var args = Array.prototype.slice.call(arguments);
            args.unshift(this.__name__ + ':');
            console.error.apply(console, args);
        };
        ClassObj.prototype.warn = function(message) {
            var args = Array.prototype.slice.call(arguments);
            args.unshift(this.__name__ + ':');
            console.warn.apply(console, args);
        };

        // вызов функции, добавляющей пользовательские методы и свойства
        class_constructor(ClassObj.prototype, parent && parent.prototype);

        return ClassObj;
    };

    window.ClassError = function ClassError(message) {
        this.message = message;
    };
    window.ClassError.prototype = new Error();


    // ======================================================================================
    //      Класс с событиями.
    //
    //      Имена событий и пространств имен не чувствительны к регистру.
    // ======================================================================================

    window.EventedObject = Class(Object, function EventedObject(cls, superclass) {
        cls.init = function() {
            this._events = {};
        };

        /*
            Освобождение ресурсов
         */
        cls.destroy = function() {
            this._events = {};
        };

        /*
            Форматирование имени события
         */
        cls._formatEventName = function(name) {
            name = $.trim(name).toLowerCase();
            if (name.indexOf(' ') >= 0) {
                this.raise('multiple events not allowed');
            }

            var name_arr = name.split('.');
            return {
                name: name_arr.shift(),
                namespaces: name_arr
            };
        };

        /*
            Добавление обработчика события
         */
        cls._addEventHandler = function(name, handler, options) {
            var evt_info = this._formatEventName(name);
            if (!evt_info.name) {
                this.error('event name not found: ' + name);
                return this;
            }

            if (!handler) {
                this.error('event handler required');
                return this;
            } else if (!$.isFunction(handler)) {
                this.error('event handler should be a function');
                return this;
            }

            var evtRecord = $.extend(options, {
                type: evt_info.name,
                handler: handler,
                namespaces: evt_info.namespaces
            });

            if (evt_info.name in this._events) {
                this._events[evt_info.name].push(evtRecord);
            } else {
                this._events[evt_info.name] = [evtRecord];
            }

            return this;
        };

        /*
            Проверка, что все namespaces содержатся в record
         */
        cls._isEveryNamespaces = function(record, namespaces) {
            if (!namespaces.length) return true;
            return namespaces.every(function(ns) {
                return record.namespaces.indexOf(ns) >= 0;
            })
        };

        /*
            Проверка, что хоть один из namespaces содержатся в record
         */
        cls._isSomeNamespaces = function(record, namespaces) {
            if (!namespaces.length) return true;
            return namespaces.some(function(ns) {
                return record.namespaces.indexOf(ns) >= 0;
            })
        };

        /*
            Удаление из стека evt_list событий evt_name, подходящих под пространства имен.
         */
        cls._removeEvents = function(evt_name, evt_list, evt_namespaces) {
            if (!evt_list || !evt_list.length) {
                return
            }

            if (!evt_namespaces.length) {
                this._events[evt_name] = [];
            } else {
                var that = this;
                this._events[evt_name] = evt_list.filter(function(record) {
                    return !that._isSomeNamespaces(record, evt_namespaces);
                });
            }
        };

        /*
            Добавление обработчика события
         */
        cls.on = function(name, handler) {
            return this._addEventHandler(name, handler, {once: false});
        };

        /*
            Добавление одноразового обработчика события
         */
        cls.one = function(name, handler) {
            return this._addEventHandler(name, handler, {once: true});
        };

        /*
            Вызов обработчиков события
         */
        cls.trigger = function() {
            var args = Array.prototype.slice.call(arguments);
            var name = args.shift();
            var evt_info = this._formatEventName(name);
            if (!evt_info.name) {
                this.error('event name not found: ' + name);
                return;
            }

            // получаем массив обработчиков
            var evt_list = this._events[evt_info.name];
            if (!evt_list) {
                return;
            }

            var i = 0;
            var record;
            var result;
            while (record = evt_list[i++]) {
                if (this._isEveryNamespaces(record, evt_info.namespaces)) {
                    var ret = record.handler.apply(this, args);
                    if (ret === false) {
                        // если один из обработчиков вернул false,
                        // trigger тоже вернет false.
                        result = false;
                    }

                    if (record.once) {
                        i--;
                        evt_list.splice(i, 1);
                    }
                }
            }

            return result;
        };

        /*
            Удаление обработчиков события
         */
        cls.off = function(name) {
            // удаление всех обработчиков
            name = $.trim(name);
            if (!name || (name == '*')) {
                this._events = {};
                return this;
            }

            var evt_info = this._formatEventName(name);
            if (evt_info.name) {
                // удаление обработчиков определенного типа
                var evt_list = this._events[evt_info.name];
                if (evt_list) {
                    this._removeEvents(evt_info.name, evt_list, evt_info.namespaces);
                }
            } else {
                // удаление по пространству имен
                for (var key in this._events) {
                    if (this._events.hasOwnProperty(key)) {
                        evt_list = this._events[key];
                        if (evt_list) {
                            this._removeEvents(key, evt_list, evt_info.namespaces);
                        }
                    }
                }
            }

            return this;
        };
    });


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
    window.Animation = Class(Object, function Animation(cls, superclass) {
        cls.defaults = {
            duration: 1000,
            delay: 20,
            easing: 'linear',
            paused: false,

            init: $.noop,
            step: $.noop,
            start: $.noop,
            stop: $.noop,
            complete: $.noop
        };


        cls.init = function(options) {
            this.opts = $.extend({}, this.defaults, options);

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

        cls.destroy = function() {
            if (!this._paused) {
                this._paused = true;
                clearInterval(this._timer);
            }

            this._deferred.reject();
        };

        // Применение шага анимации с вычислением that._progress
        cls._timerHandle = function() {
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
        cls._applyProgress = function() {
            var easeProgress = $.easing[this.opts.easing](this._progress);
            this.opts.step.call(this, easeProgress);
        };

        // Запуск анимации
        cls.start = function() {
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
        cls.stop = function(jumpToEnd) {
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
        cls.autoInit = function(name, from, to) {
            this._info = this._info || {};

            this._info[name] = {
                from: from,
                diff: to - from
            }
        };

        // Shortcut для расчета нового значения свойства
        cls.autoCalc = function(name, eProgress) {
            var info = this._info && this._info[name];
            if (!info) {
                return null
            }

            return info.from + info.diff * eProgress;
        };
    });

    $.animate = function(options) {
        return window.Animation(options);
    };

    // ======================================================================================
    //      ARRAY UTILS
    // ======================================================================================

    /*
        Поиск по массиву (или коллекции jQuery), возвращающий
        первый результат функции handler, отличный от undefined.
     */
    $.arrayFind = function(arr, handler) {
        var i, l, result;
        for (i = 0, l = arr.length; i<l; i++) {
            result = handler.call(arr[i], i, arr[i]);
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

    /*
        Добавление события на загрузку картинки.
        Если картинка уже загружена, вызовет обработчик немедленно.
        Иначе, повесит обработчик на событие "load".

        Если первым аргументом указан "true" - обработчик будет повешен в любом случае.
     */
    $.fn.onLoaded = function() {
        var permanent, callback;
        if (typeof arguments[0] == 'boolean') {
            permanent = arguments[0];
            callback = arguments[1];
        } else {
            permanent = false;
            callback = arguments[0];
        }

        if (!$.isFunction(callback)) {
            console.warn('$.onLoaded: callback required');
            return
        }

        return this.each(function(i, image) {
            if (image.tagName != 'IMG') {
                console.warn('$.onLoaded: not an image');
                return
            }

            var $image = $(image);
            if (permanent) {
                // постоянный обработчик
                $image.on('load', callback);
            }

            if ($image.prop('complete') || ($image.prop('naturalWidth') > 0)) {
                // уже загружена
                callback.call(image);
            } else if (!permanent) {
                // загрузится позже
                $image.one('load', callback);
            }
        });
    };

    // ======================================================================================
    //      DOM UTILS
    // ======================================================================================

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
        Плагин, вычисляющий максимальную высоту элементов текущей коллекции.
     */
    $.fn.getMaxHeight = function() {
        var max_height = 0;
        this.each(function(i, element) {
            var height = $(element).height();
            if (height > max_height) {
                max_height = height;
            }
        });
        return max_height;
    };


    /*
        Получение адреса картинки тэга <img> с учетом srcset
     */
    $.getSrc = function($image) {
        if (!$image.length) return;
        return $image.prop('currentSrc') || $image.prop('src');
    };


    // ======================================================================================
    //      CANVAS UTILS
    // ======================================================================================

    /*
        Класс, помогающий рассчитать размеры картинки
        при её пропорциональном ресайзе.
     */
    window.Size = Class(Object, function Size(cls, superclass) {
        cls.init = function(width, height) {
            this.width = this.source_width = parseInt(width) || 0;
            if (width <= 0) {
                return this.raise('width should be positive');
            }

            this.height = this.source_height = parseInt(height) || 0;
            if (height <= 0) {
                return this.raise('height should be positive');
            }

            this.aspect = this.width / this.height;
        };

        cls._heightByWidth = function(width) {
            return Math.floor(width / this.aspect);
        };

        cls._widthByHeight = function(height) {
            return Math.floor(height * this.aspect);
        };

        cls.setWidth = function(value) {
            value = parseInt(value) || 0;
            if (value <= 0) {
                return this.raise('width should be positive');
            }

            this.width = value;
            this.height = this._heightByWidth(value);
        };

        cls.setHeight = function(value) {
            value = parseInt(value) || 0;
            if (value <= 0) {
                return this.raise('height should be positive');
            }

            this.height = value;
            this.width = this._widthByHeight(value);
        };

        /*
            Установка ограничения по ширине
         */
        cls.maxWidth = function(value) {
            if (this.width > value) {
                this.setWidth(value);
            }
        };

        /*
            Установка ограничения по ширине
         */
        cls.maxHeight = function(value) {
            if (this.height > value) {
                this.setHeight(value);
            }
        };
    });



    /*
        Возвращает размеры canvas с учетом ограничений браузера.
        Параметры:
            img_width, img_height - исходные размеры картинки
            max_width, max_height - целевые ограничения
    */
    window.canvasSize = function(img_width, img_height, max_width, max_height) {
        var size = Size(img_width, img_height);
        if (max_width) {
            size.maxWidth(max_width);
        }
        if (max_height) {
            size.maxHeight(max_height);
        }

        // Ограничение IE
        size.maxWidth(4096);
        size.maxHeight(4096);

        // Ограничение iOS
        if ((size.width * size.height) > 5000000) {
            size.maxWidth(Math.floor(Math.sqrt(5000000 * size.aspect)));
        }

        return {
            width: size.width,
            height: size.height
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
        return df;
    };


    /*
        Создает Deferred-объект, который читает файл по URL.
     */
    $.urlReader = function(url) {
        var df = $.Deferred();

        var xhr = new XMLHttpRequest();
        xhr.open('GET', url, true);

        // Hack to pass bytes through unprocessed.
        if (xhr.overrideMimeType) {
            xhr.overrideMimeType('text/plain; charset=x-user-defined');
        }

        xhr.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                df.resolve(this.responseText);
            }
        };
        xhr.onerror = function() {
            df.reject('can not read');
        };
        xhr.send();
        return df;
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
        return df;
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

        return df;
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
            var image_size = Size(settings.coords[2], settings.coords[3]);

            var max_width = settings.max_width;
            var max_height = settings.max_height;

            // корректируем ограничения
            max_width = Math.min(max_width || target_size[0], target_size[0] || max_width);
            max_height = Math.min(max_height || target_size[1], target_size[1] || max_height);

            // Определяем размеры картинки
            if (settings.stretch) {
                // растягивать разрешено
                if (max_width) {
                    if (max_height) {
                        var max_aspect = max_width / max_height;
                        if (image_size.aspect > max_aspect) {
                            // картинка шире холста
                            image_size.setWidth(max_width)
                        } else {
                            // картинка выше холста
                            image_size.setHeight(max_height);
                        }
                    } else {
                        // плавающая выcота
                        image_size.setWidth(max_width);
                    }
                } else if (max_height) {
                    // плавающая ширина
                    image_size.setHeight(max_height);
                }
            } else {
                // растягивать запрещено
                if (max_width) {
                    image_size.maxWidth(max_width);
                }
                if (max_height) {
                    image_size.maxHeight(max_height);
                }
            }

            // Определение размера холста
            if (target_size[0] == 0) {
                target_size[0] = image_size.width;
            }
            if (target_size[1] == 0) {
                target_size[1] = image_size.height;
            }

            // Новый размер канвы
            $.extend(canvas, canvasSize(target_size[0], target_size[1]));

            // заполняем канву цветом
            context.fillStyle = 'rgba(' + settings.background.join(',') + ')';
            context.fillRect(0, 0, canvas.width, canvas.height);

            final_w = image_size.width;
            final_h = image_size.height;

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
