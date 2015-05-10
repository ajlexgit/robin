(function($) {
    var map_index = 0;

    // Конструктор карты
    var YandexMap = function($initial_input) {
        var that = this,
            input_data = $initial_input.data();

        that.id = 'ymap_'+(++map_index);

        // Форматирование координат
        that.formatCoords = function(text) {
            var coords = text.split(',').reverse();
            if (coords.length == 2)
                return coords.map(parseFloat);
            else
                return [53.510171, 49.418785]
        };


        // Получение координат по адресу
        that.addressCoords = function($input, address) {
            if (that.query) {
                that.query.abort()
            }

            that.query = $.ajax({
                url: '/yandex_maps/get_coords/',
                type: 'POST',
                data: {
                    address: address
                },
                beforeSend: function() {
                    this.cached_val = $input.val();
                    $input.prop('readonly', true).val(gettext('Please, wait...'));
                    $('.save-box button').prop('disabled', true);
                },
                success: function(response) {
                    $input.prop('readonly', false)
                        .val(response || '')
                        .change();
                    $('.save-box button').prop('disabled', false);
                },
                error: function(xhr, status, error) {
                    $input.prop('readonly', false).val(this.cached_val);
                    $('.save-box button').prop('disabled', false);

                    if (status != 'abort') {
                        alert(gettext('Address location failed'));
                    }
                }
            })
        };


        // Обновление карты при смене координат в текстовом поле
        that.refresh = function($input) {
            if (!that.map) {
                return
            }

            var coords = that.formatCoords($input.val());
            that.map.panTo(coords);
            that.point.geometry.setCoordinates(coords);
        };


        // Создаем DIV для карты
        var map_container = $('<div/>').attr('id', that.id);
        if (input_data.width) {
            map_container.width(input_data.width)
        }
        map_container.height(input_data.height || '300px');
        map_container.css('margin-top', '10px');
        $initial_input.parent().append(map_container);

        ymaps.ready(function() {
            var center = that.formatCoords($initial_input.val());

            that.map = new ymaps.Map(that.id, {
                center: center,
                zoom: 15,
                type: 'yandex#publicMap',
                behaviors: ['default', 'scrollZoom']
            });

            that.map.controls.add('zoomControl');
            that.map.controls.add('mapTools');
            that.map.controls.add('typeSelector');

            that.map.events.add('dblclick', function(e) {
                // Перемещаем метку при двойном клике
                e.preventDefault();
                var coords = e.get('coords').map(function(coord) {
                    return coord.toFixed(6)
                });

                that.point.geometry.setCoordinates(coords);
                $initial_input.val(coords.reverse().join(', '));
            });

            that.point = new ymaps.Placemark(center, {
                balloonContentHeader: 'My point',
                balloonContentBody: 'Be happy :)'
            }, {
                draggable: true
            });
            that.point.events.add('dragend', function() {
                // Событие конца перетаскивания метки
                var coords = that.point.geometry.getCoordinates().map(function(coord) {
                    return coord.toFixed(6)
                }).reverse().join(', ');
                $initial_input.val(coords)
            });
            that.map.geoObjects.add(that.point)
        });
    };


    // Инициализация карты
    window.init_yandex_map = function() {
        var self = $(this);

        if (self.closest('.empty-form').length) {
            return
        }

        self.data('map', new YandexMap(self));
    };


    $(document).ready(function() {
        // Инициализация всех карт на странице
        $('.ymap_field').each(init_yandex_map);

        // Инициализация карт после добавления инлайна с картой
        if (window.Suit) {
            Suit.after_inline.register('add_inline', function(inline_prefix, row){
                row.find('.ymap_field').each(init_yandex_map);
            })
        }
    });


    // Изменение карты при изменении координат в текстовом поле
    $(document).on('change', '.ymap_field', function() {
        var self = $(this),
            map = self.data('map');

        if (map) {
            map.refresh(self)
        }
    });

})(jQuery);
