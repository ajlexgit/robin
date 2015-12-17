(function($) {

    $(document).ready(function() {
        $.visibilityInspector.inspect('.layer');

        $('.layer').layer({
            onInit: function() {
                this.$container = $('#layer-sticky').find('.area');
            },
            calcOffset: function(win_scroll) {
                var container_top = this.$container.offset().top;
                var container_height = this.$container.outerHeight();
                var win_height = document.documentElement.clientHeight;

                var from_point = container_top - win_height;
                var to_point = container_top + container_height;

                if ((win_scroll >= from_point) && (win_scroll <= to_point)) {
                    return this._initial + parseInt(0.5 * (win_scroll - from_point));
                } else {
                    return false;
                }
            }
        }).on('appear', function() {
            console.log('block became visible');
        }).on('disappear', function() {
            console.log('block became invisible');
        });

        // sticky
        $('.sticky').sticky({

        });

        // parallax
        $('#parallax').parallax({

        });
    });


    // gmap
    GMap.ready(function() {
        var gmapStyles = [
            {
                "featureType": "all",
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
                "featureType": "landscape.natural",
                "stylers": [
                    {"visibility": "on"},
                    {"color": "#d3e5b6"}
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


        window.gmap = GMap('#gmap .map', {
            center: GMapPoint(53.510171, 49.418785),
            styles: gmapStyles,
            zoom: 2
        }).on('ready', function() {
            var marker = GMapMarker({
                map: this,
                position: GMapPoint(62.281819, -150.287132),
                hint: 'First'
            });

            var overlay = GMapImageTripleOverlay({
                map: this,
                src: 'http://kompozer.net/images/svg/Mozilla_Firefox.svg',
                coords: {
                    bottomleft: GMapPoint(62.281819, -150.287132),
                    topright: GMapPoint(62.400471, -150.287132)
                }
            });

            this.center(GMapPoint(62.281819, -150.287132)).zoom(11);
        });
    });

})(jQuery);
