(function ($) {
    var map_index = 0;

    window.init_google_map = function() {
        // Инициализация одной карты
        var gmap_id = 'gmap_' + (++map_index),
            gmap_div = $(this).attr('id', gmap_id),
            gmap_div_data = gmap_div.data();

        var center = new google.maps.LatLng(
            parseFloat(gmap_div_data.lat) || 53.510171,
            parseFloat(gmap_div_data.lng) || 49.418785
        );

        var map = new google.maps.Map(this, {
            zoom: parseInt(gmap_div_data.zoom) || 14,
            center: center
        });

        var marker = new google.maps.Marker({
            map: map,
            position: center
        });

        // Baloon
        var content = '';
        if (gmap_div_data.header) {
            content += '<h3 style="font: 20px Arial, Helvetica, sans-serif">' + gmap_div_data.header + '</h3>';
        }
        if (gmap_div_data.content) {
            content += '<p>' + gmap_div_data.content + '</p>';
        }
        if (content) {
            var infowindow = new google.maps.InfoWindow({
                content: content
            });

            google.maps.event.addListener(marker, 'click', function () {
                infowindow.open(map, marker);
            });
        }
    };


    window.init_google_maps = function() {
        // Инициализация всех карт на странице
        $('.google-map').each(window.init_google_map);
    };

    $(document).ready(function() {
        var script = document.createElement('script');
        script.type = 'text/javascript';
        script.src = 'https://maps.googleapis.com/maps/api/js?v=3.exp&callback=init_google_maps';
        document.body.appendChild(script);
    });

})(jQuery);
