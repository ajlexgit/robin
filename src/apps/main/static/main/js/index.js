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
        var gmapStyle = [
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
            zoom: 2
        }).on('ready', function() {
            console.log('ready');
            var marker = GMapMarker({
                map: this,
                position: this.center()
            })
        });

            /*map_options: {
                styles: gmapStyle
            },
            onInit: function() {
                this.addPlacemark({
                    lng: 49.418785,
                    lat: 53.510171,
                    hint: 'First',
                    balloon: '<p>Hello</p>'
                });

                this.addPlacemark({
                    lng: -45.72308,
                    lat: -21.216105,
                    hint: 'second',
                    draggable: true,
                    balloon: '<p>Goodbay</p>'
                });

                this.setCenter(this.getPoints());

                // intact
                /*var intactSubdomains = [
                    "0",
                    "1",
                    "2",
                    "3"
                ];
                var intactIndex = 0;
                var getIntactHost = function() {
                    var cdn = intactSubdomains[intactIndex++ % intactSubdomains.length];
                    return 'http://' + cdn + '.ashbu.cartocdn.com/wri-01/api/v1/map/b92e0fecd7d27e8114973cf095c9d3f0:1444468359441.9302/'
                };
                var intactTile = {
                    getTileUrl: function(coord, zoom) {
                        return [
                            getIntactHost(),
                            zoom,
                            '/',
                            coord.x,
                            '/',
                            coord.y,
                            '.png'
                        ].join('');
                    },
                    tileSize: new google.maps.Size(256, 256) // or whatever
                };
                this.map.overlayMapTypes.insertAt(0, new google.maps.ImageMapType(intactTile));

                // tropical
                var tropicalSubdomains = ["3"];
                var tropicalIndex = 0;
                var getTropicalHost = function() {
                    var cdn = tropicalSubdomains[tropicalIndex++ % tropicalSubdomains.length];
                    return 'https://s' + cdn + '.amazonaws.com/wri-tiles/tropicalcarbonstock/'
                };
                var tropicalTile = {
                    getTileUrl: function(coord, zoom) {
                        return [
                            getTropicalHost(),
                            zoom,
                            '/',
                            coord.x,
                            '/',
                            coord.y,
                            '.png'
                        ].join('');
                    },
                    tileSize: new google.maps.Size(256, 256) // or whatever
                };
                this.map.overlayMapTypes.insertAt(0, new google.maps.ImageMapType(tropicalTile));
            }
        });*/
    });

})(jQuery);
