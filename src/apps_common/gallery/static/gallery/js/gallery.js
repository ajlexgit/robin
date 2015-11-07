(function($) {

    $(document).ready(function() {
        $('.gallery').each(function() {
            Gallery.create(this, {
                itemSelector: '.gallery-item'
            });
        })
    })

})(jQuery);
