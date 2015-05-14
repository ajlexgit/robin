(function($) {

    /*
        Обертка над функцией, которая выполняется не чаще,
        чем раз в time миллисекунд.
    */

    $.rared = function(callback, time) {
        var blocked;
        return function() {
            if (blocked) return;

            callback.apply(this, arguments);

            blocked = true;
            setTimeout(function () {
                blocked = false
            }, time);
        }
    };

})(jQuery);