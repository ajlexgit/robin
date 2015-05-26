(function($){

    $.fn.visible = function(direction) {
        if (this.length < 1) {
            return;
        }

        var elem = this.get(0),
            vpWidth = document.documentElement.clientWidth,
            vpHeight = document.documentElement.clientHeight,
            rec = elem.getBoundingClientRect(),

            topInviz = rec.top > vpHeight,
            bottonInviz = rec.bottom < 0,
            leftInviz = rec.left > vpWidth,
            rightInviz = rec.right < 0,

            vVisible = !(topInviz || bottonInviz),
            hVisible = !(leftInviz || rightInviz);

        direction = direction || 'both';
        if (direction === 'both')
            return vVisible && hVisible;
        else if (direction === 'vertical')
            return vVisible;
        else if (direction === 'horizontal')
            return hVisible;
    };

})(jQuery);
