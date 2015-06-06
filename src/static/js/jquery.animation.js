/**
* Provides requestAnimationFrame in a cross browser way.
* http://paulirish.com/2011/requestanimationframe-for-smart-animating/
*/
(function($) {

    var handler = window.requestAnimationFrame ||
        window.webkitRequestAnimationFrame ||
        window.mozRequestAnimationFrame ||
        window.oRequestAnimationFrame ||
        window.msRequestAnimationFrame ||
        function(callback) {
            window.setTimeout(callback, 1000 / 60);
        };

    $.animation_frame = function(callback, element) {
        return $.proxy(handler, window, callback, element)
    };

    // Animate
    $.animate = function(options) {
        var settings = $.extend({
            duration: 1000,
            easing: 'linear',
            init: $.noop,
            step: $.noop,
            complete: $.noop
        }, options);
        
        settings.duration = Math.max(settings.duration, 20);
        settings.init.call(settings);
        
        var start = $.now();
        var timer = setInterval(function() {
            var progress = ($.now() - start) / settings.duration;
            if (progress >= 1) {
                progress = 1;
                clearInterval(timer);
            }

            var easeProgress = $.easing[settings.easing](progress);
            settings.step.call(settings, easeProgress, progress);
            
            if (progress === 1) {
                settings.complete.call(settings);
            }
        }, 20);
        return timer;
    };
    
})(jQuery);