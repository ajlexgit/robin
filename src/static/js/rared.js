(function($) {

    /*

        Обертка над функцией, которая выполняется не чаще,
        чем раз в time миллисекунд.

    */

    $.rared = function(callback, time) {
        var timer, that, args;
        return function() {
            that = this;
            args = arguments;
            if (timer) return false;
            timer = setTimeout(function() {
                callback.apply(that, args);
                timer = null;
            }, time);
        }
    };

})(jQuery);