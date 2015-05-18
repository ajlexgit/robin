/**
* Provides requestAnimationFrame in a cross browser way.
* http://paulirish.com/2011/requestanimationframe-for-smart-animating/
*/
(function() {
    
    $.animation_frame = window.requestAnimationFrame ||
        window.webkitRequestAnimationFrame ||
        window.mozRequestAnimationFrame ||
        window.oRequestAnimationFrame ||
        window.msRequestAnimationFrame ||
        function(callback, element) {
            window.setTimeout(callback, 1000 / 60);
        }
    
})(jQuery);