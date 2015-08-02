(function($) {

    $(document).ready(function() {
        $('.gallery').each(function() {
            new Gallery(this, {
                itemSelector: '.gallery-item'
            });
        })
    })

})(jQuery);
