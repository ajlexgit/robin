(function($) {

    /*
        Регистратор обработчиков, выполняющихся при
        достижении браузером определенного интервала по ширине.

        Требует:
            jquery.utils.js

        Параметры:
            min     - нижняя граница интервала (включительно)
            mix     - верхняя граница интервала (НЕ включительно)

     */
    var intervals = [];
    window.MediaInterval = Class(null, function(cls, superclass) {
        cls.init = function(min, max) {
            if (typeof min != 'number') {
                console.error('MediaInterval: lower bound should be a number');
                return false;
            } else if (min < 0) {
                console.error('MediaInterval: lower bound should be non-negative');
                return false;
            }

            if (typeof max != 'number') {
                console.error('MediaInterval: upper bound should be a number');
                return false;
            } else if (max < 0) {
                console.error('MediaInterval: upper bound should be non-negative');
                return false;
            }

            if ((max != 0) && (min >= max)) {
                console.error('MediaInterval: lower bound must be lower than upper bound');
                return false;
            }

            this._min = min;
            this._max = max;
            this._events = {};

            intervals.push(this);
        };

        /*
            Возвращает true, если точка входит в интервал
         */
        cls.prototype.contains = function(point) {
            return point >= this._min && ((this._max == 0) || (point < this._max));
        };

        /*
            Уничтожение всех обработчиков и прекращение отслеживания событий
         */
        cls.prototype.destroy = function() {
            var that = this;
            var index = $.arrayFind(intervals, function(index, item) {
                return (item === that) && index;
            });

            if (index >= 0) {
                intervals.splice(index, 1);
            }

            this._events = {};
        };

        /*
            Добавление обработчика входа в интервал
         */
        cls.prototype.enter = function() {
            if ('enter' in this._events) {
                Array.prototype.concat.apply(this._events.enter, arguments);
            } else {
                this._events.enter = Array.apply(null, arguments);
            }
            return this;
        };

        /*
            Добавление обработчика выхода из интервала
         */
        cls.prototype.leave = function() {
            if ('leave' in this._events) {
                Array.prototype.concat.apply(this._events.leave, arguments);
            } else {
                this._events.leave = Array.apply(null, arguments);
            }
            return this;
        };

        /*
            Выполнение обработчиков события
         */
        cls.prototype.trigger = function(event, point) {
            if (typeof event != 'string') {
                console.error('MediaInterval: event name should be a string');
                return this;
            }

            if (event in this._events) {
                $.each(this._events[event], function(i, handler) {
                    handler(point);
                })
            }
        };

        /*
            Удаление обработчика.
            Если аргумент не передан - удалит все обработчики интервала
         */
        cls.prototype.off = function(event) {
            if (event === undefined) {
                this._events = {};
                return this;
            }

            if (typeof event != 'string') {
                console.error('MediaInterval: event name should be a string');
                return this;
            }

            if (event in this._events) {
                delete this._events;
            } else {
                console.debug('MediaInterval: events "' + event + '" are not registered');
            }

            return this;
        };
    });

    var old_width = window.innerWidth;

    $(document).ready(function() {
        $.each(intervals, function(i, interval) {
            if (interval.contains(window.innerWidth)) {
                interval.trigger('enter', window.innerWidth);
            } else {
                interval.trigger('leave', window.innerWidth);
            }
        });
    });

    $(window).on('resize.media_interval', $.rared(function() {
        $.each(intervals, function(i, interval) {
            if (interval.contains(window.innerWidth)) {
                if (isNaN(old_width) || !interval.contains(old_width)) {
                    interval.trigger('enter', window.innerWidth);
                }
            } else {
                if (!isNaN(old_width) && interval.contains(old_width)) {
                    interval.trigger('leave', window.innerWidth);
                }
            }
        });

        old_width = window.innerWidth;
    }, 60));

})(jQuery);