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

    var getMediaPoint = function() {
        return window.innerWidth;
    };

    var intervals = [];
    var old_point = getMediaPoint();

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
            Возвращает true, если текущая ширна окна входит в интервал
         */
        cls.prototype.is_active = function() {
            return this.contains(getMediaPoint());
        };

        /*
            Уничтожение всех обработчиков и прекращение отслеживания событий
         */
        cls.prototype.destroy = function() {
            this._events = {};

            var index = intervals.indexOf(this);
            if (index >= 0) {
                intervals.splice(index, 1);
            }
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

    $(window).on('resize.media_interval', $.rared(function() {
        var current_point = getMediaPoint();

        $.each(intervals, function(i, interval) {
            if (interval.contains(current_point)) {
                if (!interval.contains(old_point)) {
                    interval.trigger('enter', current_point);
                }
            } else {
                if (interval.contains(old_point)) {
                    interval.trigger('leave', current_point);
                }
            }
        });

        old_point = window.innerWidth;
    }, 100));

})(jQuery);