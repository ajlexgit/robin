(function($) {

    /*
         Регистратор обработчиков, выполняющихся при
         достижении браузером определенного интервала по ширине.
     */

    window.MediaEvents = Class(null, function(cls, superclass) {
        cls.init = function() {
            this.current_ingexes = [];
            this.triggers = [];
            this.handlers = [];
        };

        /*
            Добавление обработчика, остлеживающего
            заданный интервал ширины окна браузера.
         */
        cls.prototype.register = function(min, max, handler) {

        }
    });

})(jQuery);