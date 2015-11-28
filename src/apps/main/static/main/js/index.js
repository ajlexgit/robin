(function($) {

    $(document).ready(function() {
        $('.custom-counter').counter({
            min: 0,
            max: 5,
            beforeChange: function(value) {
                console.log(value);
            }
        }).on('change', function() {
            console.log('ch')
        });
    })

})(jQuery);
