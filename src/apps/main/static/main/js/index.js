(function($) {

    $(document).ready(function() {
        $.visibilityInspector.inspect('.layer');

        $('.layer').layer({
            speed: 0.75
        }).on('appear', function() {
            console.log('block became visible');
        }).on('disappear', function() {
            console.log('block became invisible');
        });

        $('.sticky').sticky({

        });

        $('#parallax').parallax({

        });
    })

})(jQuery);
