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
    });


    // gmap
    GMap.ready(function() {
        var gmapStyles = [
            {
                "featureType": "administrative",
                "stylers": [
                    {"visibility": "off"}
                ]
            },
            {
                "featureType": "administrative.country",
                "stylers": [
                    {"visibility": "on"}
                ]
            },
            {
                "featureType": "landscape.man_made",
                "stylers": [
                    {"visibility": "off"}
                ]
            },
            {
                "featureType": "landscape.natural",
                "stylers": [
                    {"visibility": "on"},
                    {"color": "#efefef"}
                ]
            },
            {
                "featureType": "poi",
                "stylers": [
                    {"visibility": "off"}
                ]
            },
            {
                "featureType": "road",
                "stylers": [
                    {"visibility": "off"}
                ]
            },
            {
                "featureType": "transit",
                "stylers": [
                    {"visibility": "off"}
                ]
            },
            {
                "featureType": "water"
            }
        ];


        window.gmap = GMap('#gmap', {
            center: GMapPoint(53.510171, 49.418785),
            styles: gmapStyles,
            zoom: 2
        }).on('ready', function() {
            var marker1 = GMapMarker({
                map: this,
                position: GMapPoint(53.510171, 49.418785),
                hint: 'First',
                balloon: '<p>Hello</p>'
            });

            var marker2 = GMapMarker({
                map: this,
                position: GMapPoint(-30, 30),
                hint: 'second',
                draggable: true,
                balloon: '<p>Goodbay</p>'
            });

            this.center(this.markers[0].position());
        });
    });

})(jQuery);
