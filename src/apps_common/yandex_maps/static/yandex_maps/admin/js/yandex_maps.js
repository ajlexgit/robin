(function($) {

    // Получение координат из строки "lng, lat"
    var text2coords = function(text) {
        var coords = text.split(',');
        if (coords.length == 2)
            coords = coords.map(parseFloat).reverse();
        else
            coords = [53.510171, 49.418785];

        return coords;
    };


    // Получение текста координат
    var coords2text = function(coords) {
        return coords.map(function(coord) {
            return coord.toFixed(6)
        }).reverse().join(', ')
    };


    var init_map_field = function() {
        var $field = $(this);
        if ($field.closest('.empty-form').length) {
            return
        }

        // Создание контейнера для карты
        var field_data = $field.data();
        var $map = $('<div>').addClass('yandex-map');
        if (field_data.width) {
            $map.width(field_data.width)
        }
        $map.height(field_data.height || '300px');
        $map.css('margin-top', '10px');
        $field.after($map);

        // карта
        YandexMap.create($map, {
            map_options: {
                behaviors: ["drag", "multiTouch"],
                zoom: 16
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

                this.setCenter(point);

                // установка значения поля при двойном клике
                var that = this;
                this.addListener(this.map, 'dblclick', function(evt) {
                    evt.preventDefault();
                    var point = evt.get('coords');
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
            Suit.after_inline.register('yandex_map_inline', function(inline_prefix, row) {
                row.find('.yandex-map-field').each(init_map_field);
            })
        }
    }).on('yandex-maps-ready', function() {
        // Инициализация всех карт на странице
        $('.yandex-map-field').each(init_map_field);
    }).on('change', '.yandex-map-field', function() {
        // Изменение карты при изменении координат в текстовом поле
        var $field = $(this);
        var ymap = $field.next('.yandex-map').data('map');

        var point = text2coords($field.val());
        var placemark = ymap.getPlacemark();
        placemark.moveTo(point);
        ymap.panTo(point);
    });

})(jQuery);
