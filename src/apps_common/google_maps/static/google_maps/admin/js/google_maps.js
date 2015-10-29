(function($) {

    // Получение координат из строки "lng, lat"
    var text2coords = function(text) {
        var coords = text.split(',');
        if (coords.length == 2)
            coords = coords.map(parseFloat);
        else
            coords = [49.418785, 53.510171];

        return new google.maps.LatLng(coords[1], coords[0]);
    };

    // Получение текста координат
    var coords2text = function(coords) {
        coords = [coords.lng(), coords.lat()];
        return coords.map(function(coord) {
            return coord.toFixed(6)
        }).join(', ')
    };

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
        var gmap = GoogleMap.create($map, {
            map_options: {
                disableDoubleClickZoom: true,
                zoom: 15
            }
        });

        // точка
        var point = text2coords($field.val());
        gmap.setCenter(point);
        gmap.marker = gmap.createMarker(point, {
            draggable: true
        });

        // установка значения поля при перемещение маркера
        gmap.addListener(gmap.marker, 'dragend', function() {
            var point = this.marker.getPosition();
            $field.val(coords2text(point));
        });

        // установка значения поля при войном клике
        gmap.addListener(gmap.map, 'dblclick', function(evt) {
            var point = evt.latLng;
            this.marker.setPosition(point);
            $field.val(coords2text(point));
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
        var $map = $field.next('.google-map');
        var gmap = $map.data('map');

        var point = text2coords($field.val());
        gmap.panTo(point);
        gmap.marker.setPosition(point);
    });

})(jQuery);
