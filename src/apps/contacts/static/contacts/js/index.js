(function($) {

    var gmap;

    // получение точки по jQuery-объекту адреса
    var pointByAddr = function($address) {
        var addr_data = $address.data();
        return GMapPoint(addr_data.lat, addr_data.lng);
    };

    // клик на адрес
    $(document).on('click', '.address', function() {
        var $address = $(this);
        var point = pointByAddr($address);
        if (point && gmap) {
            gmap.center(point);

            // маркер по центру непокрытой области
            gmap.panBy(0, -$('.overlay').outerHeight() / 2);

            var marker = gmap.markers[0];
            if (marker) {
                marker.position(point);
                marker.label($address.find('[itemprop="streetAddress"]').text());
            }

            $address.addClass('active').siblings().removeClass('active');
        }
    });

    $(document).ready(function() {
        var $addresses = $('#addresses').find('.address');
        if ($addresses.length) {
            var $first = $addresses.first();

            gmap = GMap('#google-map .map', {
                center: pointByAddr($first),
                zoom: 15
            }).on('ready', function() {
                GMapMarker({
                    map: this,
                    position: this.center(),
                    label: $first.find('[itemprop="streetAddress"]').text()
                });

                $first.addClass('active');
            }).on('resize', function() {
                var marker = this.markers[0];
                if (marker) {
                    this.center(marker);

                    // маркер по центру непокрытой области
                    this.panBy(0, -$('.overlay').outerHeight() / 2);
                }
            });
        }
    });

})(jQuery);
