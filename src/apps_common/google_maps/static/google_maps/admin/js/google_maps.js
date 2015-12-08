(function($) {

    var init_map_field = function() {
        var $field = $(this);
        if ($field.closest('.empty-form').length) {
            return
        }

        // Создание контейнера для карты
        var field_data = $field.data();
        var $map = $('<div>').addClass('google-map');
        if (field_data.width) {
            $map.width(field_data.width)
        }
        $map.height(field_data.height || '300px');
        $map.css('margin-top', '10px');
        $field.after($map);

        // карта
        var gmap = GMap($map, {
            zoom:16
        }).on('ready', function() {
            var point = GMapPoint.fromString($field.val());
            if (!point) {
                return
            }

            var marker = GMapMarker({
                map: this,
                position: point,
                draggable: true
            }).on('dragend', function() {
                $field.val(this.position().toString());
            });

            this.center(point);

            // установка значения поля при двойном клике
            this.on('dblclick', function(evt) {
                var point = GMapPoint(evt.latLng.lat(), evt.latLng.lng());
                marker.position(point);
                $field.val(point.toString());
            });
        });
    };


    $(document).ready(function() {
        // Инициализация карт после добавления инлайна с картой
        if (window.Suit) {
            Suit.after_inline.register('google_map_inline', function(inline_prefix, row) {
                row.find('.google-map-field').each(init_map_field);
            })
        }
    }).on('google-maps-ready', function() {
        // Инициализация всех карт на странице
        $('.google-map-field').each(init_map_field);
    }).on('change', '.google-map-field', function() {
        // Изменение карты при изменении координат в текстовом поле
        var $field = $(this);
        var gmap = $field.next('.google-map').data(GMap.dataParamName);

        var point = GMapPoint.fromString($field.val());
        var marker = gmap.markers[0];
        if (marker) {
            marker.position(point);
        }
        gmap.panTo(point);
    });

})(jQuery);
