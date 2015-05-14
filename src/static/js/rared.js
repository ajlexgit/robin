(function($) {

    /*
        Обертка над функцией, которая выполняется не чаще,
        чем раз в time миллисекунд.
    */

    $.rared = function(callback, time) {
        var blocked, that, args;
        return function() {
            that = this;
            args = arguments;

            if (blocked) return;

            callback.apply(that, args);

            blocked = true;
            setTimeout(function() {
                blocked = false;
                callback.apply(that, args);
            }, time);
        }
    };

})(jQuery);