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
        GoogleMap.create($map, {
            map_options: {
                disableDoubleClickZoom: true,
                zoom: 15
            },
            onInit: function() {
                var point = text2coords($field.val());

                this.addPlacemark({
                    point: point,
                    draggable: true,
                    onDragEnd: function() {
                        $field.val(coords2text(this.point));
                    }
                });

                this.setCenter(this.getPoints());

                // установка значения поля при двойном клике
                var that = this;
                this.addListener(this.map, 'dblclick', function(evt) {
                    var point = evt.latLng;
                    var placemark = that.getPlacemark();
                    placemark.moveTo(point);
                    $field.val(coords2text(point));
                });
            }
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
        var gmap = $field.next('.google-map').data('map');

        var point = text2coords($field.val());
        var placemark = gmap.getPlacemark();
        placemark.moveTo(point);
        gmap.panTo(point);
    });

})(jQuery);
