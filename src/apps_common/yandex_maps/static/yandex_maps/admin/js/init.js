(function($) {

    var map_index = 0;

    // Получение координат из строки "lng, lat"
    var text2coords = function(text) {
        var coords = text.split(',');
        if (coords.length == 2)
            return coords.map(parseFloat);
        else
            return [53.510171, 49.418785];
    };

    // Получение текста координат
    var coords2text = function(coords) {
        return coords.map(function (coord) {
            return coord.toFixed(6)
        }).join(', ')
    };

    var YandexMap = function($field, $map) {
        var that = this;

        // Получение координат по адресу
        that.addressCoords = function(address) {
            if (that.query) {
                that.query.abort();
            }

            that.query = $.ajax({
                url: '/yandex_maps/get_coords/',
                type: 'POST',
                data: {
                    address: address
                },
                beforeSend: function() {
                    // Блокировка кнопок при запросе
                    this.old_val = $field.val();
                    $field.prop('readonly', true).val(gettext('Please, wait...'));
                    $('.save-box button').prop('disabled', true);
                },
                success: function(response) {
                    $field.val(response || '').change();
                },
                error: function(xhr, status, error) {
                    $field.val(this.old_val);
                    if (status != 'abort') {
                        alert(gettext('Address location failed'));
                    }
                },
                complete: function() {
                    $field.prop('readonly', false);
                    $('.save-box button').prop('disabled', false);
                }
            });
        };

        // Установка ID карты
        var ymap_id = 'ymap_' + (++map_index);
        $map.attr('id', ymap_id);

        that.center = text2coords($field.val());

        that.map = new ymaps.Map(ymap_id, {
            center: that.center,
            zoom: 14,
            behaviors: ['default', 'scrollZoom']
        });

        that.map.controls.add('zoomControl');
        that.map.controls.add('mapTools');
        that.map.controls.add('typeSelector');

        // Создание маркера
        that.marker = new ymaps.Placemark(that.center, {
            balloonContentHeader: 'My point',
            balloonContentBody: 'Be happy :)'
        }, {
            draggable: true
        });

        // Отображение координат в поле при перетаскивании маркера
        that.marker.events.add('dragend', function() {
            var coords = that.marker.geometry.getCoordinates();
            $field.val(coords2text(coords));
        });

        // Отображение координат в поле при двойном клике на карте
        that.map.events.add('dblclick', function(e) {
            var coords = e.get('coords');
            that.marker.geometry.setCoordinates(coords);
            $field.val(coords2text(coords));
            e.preventDefault();
        });

        that.map.geoObjects.add(that.marker);
    };

    var init_map_field = function() {
        var $field = $(this);
        var field_data = $field.data();
        if ($field.closest('.empty-form').length) {
            return
        }

        if ($field.hasClass('map-inited')) {
            return
        } else {
            $field.addClass('map-inited');
        }

        // Создание контейнера для карты
        var $map = $('<div>');
        if (field_data.width) {
            $map.width(field_data.width)
        }
        $map.height(field_data.height || '300px');
        $map.css('margin-top', '10px');
        $field.after($map);

        $map.data('map', new YandexMap($field, $map));
    };

    window.init_yandex_maps = function() {
        $(document).trigger('yandex-maps-ready');
    };

    $(document).ready(function() {
        var lang = $(document.documentElement).attr('lang');

        var script = document.createElement('script');
        script.type = 'text/javascript';
        script.src = '//api-maps.yandex.ru/2.0-stable/?load=package.standard&onload=init_yandex_maps&lang=' + lang;
        document.body.appendChild(script);

        // Инициализация карт после добавления инлайна с картой
        if (window.Suit) {
            Suit.after_inline.register('yandex_map_inline', function(inline_prefix, row) {
                row.find('.yandex-map').each(init_map_field);
            })
        }
    }).on('yandex-maps-ready', function() {
        // Инициализация всех карт на странице
        $('.yandex-map').each(init_map_field);
    }).on('change', '.yandex-map', function() {
        // Изменение карты при изменении координат в текстовом поле
        var $field = $(this);
        var $map = $field.next('div');
        var map_object = $map.data('map');

        var coords = text2coords($field.val());
        map_object.map.panTo(coords);
        map_object.marker.geometry.setCoordinates(coords);
    });

})(jQuery);
