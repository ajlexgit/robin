(function ($) {

    /*
        Центрирование карты гугла при ресайзе:
            $(document).on('google-maps-ready', function() {
                google.maps.event.addDomListener(window, 'resize', $.rared(function() {
                    $('.google-map').each(function () {
                        var gmap = $(this).data('map');
                        gmap.map.setCenter(gmap.center);
                    });
                }, 300));
            });
    */

    var GoogleMap = function($map) {
        var that = this;
        var map_data = $map.data();

        that.center = new google.maps.LatLng(
            parseFloat(map_data.lat) || 53.510171,
            parseFloat(map_data.lng) || 49.418785
        );

        that.map = new google.maps.Map($map.get(0), {
            zoom: parseInt(map_data.zoom) || 14,
            center: that.center
        });

        that.marker = new google.maps.Marker({
            map: that.map,
            position: that.center
        });
    };

    window.init_google_maps = function() {
        $(document).trigger('google-maps-ready');
    };

    $(document).ready(function() {
        var lang = $(document.documentElement).attr('lang');
        var script = document.createElement('script');
        script.src = 'https://maps.googleapis.com/maps/api/js?v=3.exp&callback=init_google_maps&language=' + lang;
        document.body.appendChild(script);
    }).on('google-maps-ready', function() {
        // Инициализация всех карт на странице
        $('.google-map').each(function() {
            var $this = $(this);
            $this.data('map', new GoogleMap($this));
        });
    });

})(jQuery);
