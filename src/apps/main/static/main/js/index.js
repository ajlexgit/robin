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
                    {"color": "#d3e5b6"}
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
                "featureType": "water",
                "stylers": [
                    {"visibility": "on"},
                    {"color": "#ffffff"}
                ]
            }
        ];


        window.gmap = GMap('#gmap', {
            center: GMapPoint(53.510171, 49.418785),
            styles: gmapStyles,
            zoom: 2
        }).on('ready', function() {
            var marker1 = GMapMarker({
                map: this,
                position: GMapPoint(62.281819, -150.287132),
                hint: 'First',
                balloon: '<p>Hello</p>'
            });

            var marker2 = GMapMarker({
                map: this,
                position: GMapPoint(62.400471, -150.005608),
                hint: 'second',
                draggable: true,
                balloon: '<p>Goodbay</p>'
            });

            var overlay = GMapOverlay({
                map: this,
                src: 'https://developers.google.com/maps/documentation/javascript/examples/full/images/talkeetna.png',
                coords: {
                    bottomleft: GMapPoint(62.281819, -150.287132),
                    topright: GMapPoint(62.400471, -150.005608)
                }
            });

            this.center(GMapPoint(62.339889, -150.145683)).zoom(11);
        });
    });

})(jQuery);
