(function ($) {

    // Получение координат из строки "lng, lat"
    var text2coords = function (text) {
        var coords = text.split(',').reverse();
        if (coords.length == 2)
            coords = coords.map(parseFloat);
        else
            coords = [53.510171, 49.418785];

        return new google.maps.LatLng(coords[0], coords[1]);
    };

    // Получение текста координат
    var coords2text = function (coords) {
        return coords.map(function (coord) {
            return coord.toFixed(6)
        }).reverse().join(', ')
    };

    // TODO
    var GoogleMap = function ($field, $map) {
        var that = this;

        console.log($field, $map);
        that.center = text2coords($field.val());

        that.map = new google.maps.Map($map.get(0), {
            zoom: 14,
            center: that.center
        });

        that.marker = new google.maps.Marker({
            map: that.map,
            position: that.center
        });

        //// Получение координат по адресу
        //that.addressCoords = function (address) {
        //    if (that.query) {
        //        that.query.abort();
        //    }
        //
        //    that.query = $.ajax({
        //        url: '/google_maps/get_coords/',
        //        type: 'POST',
        //        data: {
        //            address: address
        //        },
        //        beforeSend: function () {
        //            // Блокировка кнопок при запросе
        //            this.old_val = $field.val();
        //            $field.prop('readonly', true).val(gettext('Please, wait...'));
        //            $('.save-box button').prop('disabled', true);
        //        },
        //        success: function (response) {
        //            $field.val(response || '').change();
        //        },
        //        error: function (xhr, status, error) {
        //            $field.val(this.old_val);
        //            if (status != 'abort') {
        //                alert(gettext('Address location failed'));
        //            }
        //        },
        //        complete: function () {
        //            $field.prop('readonly', false);
        //            $('.save-box button').prop('disabled', false);
        //        }
        //    });
        //};
        //
        //that.map.controls.add('zoomControl');
        //that.map.controls.add('mapTools');
        //that.map.controls.add('typeSelector');
        //
        //// Создание маркера
        //that.marker = new ymaps.Placemark(that.center, {
        //    balloonContentHeader: 'My point',
        //    balloonContentBody: 'Be happy :)'
        //}, {
        //    draggable: true
        //});
        //
        //// Отображение координат в поле при перетаскивании маркера
        //that.marker.events.add('dragend', function () {
        //    var coords = that.marker.geometry.getCoordinates();
        //    $field.val(coords2text(coords));
        //});
        //
        //// Отображение координат в поле при двойном клике на карте
        //that.map.events.add('dblclick', function (e) {
        //    var coords = e.get('coords');
        //    that.marker.geometry.setCoordinates(coords);
        //    $field.val(coords2text(coords));
        //    e.preventDefault();
        //});
        //
        //that.map.geoObjects.add(that.marker);
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

        $map.data('map', new GoogleMap($field, $map));
    };

    window.init_google_maps = function() {
        $(document).trigger('google-maps-ready');
    };

    $(document).ready(function() {
        var lang = $(document.documentElement).attr('lang');

        var script = document.createElement('script');
        script.type = 'text/javascript';
        script.src = 'https://maps.googleapis.com/maps/api/js?v=3.exp&callback=init_google_maps&language=' + lang;
        document.body.appendChild(script);

        // Инициализация карт после добавления инлайна с картой
        if (window.Suit) {
            Suit.after_inline.register('google_map_inline', function(inline_prefix, row) {
                row.find('.google-map').each(init_map_field);
            })
        }
    }).on('google-maps-ready', function() {
        // Инициализация всех карт на странице
        $('.google-map').each(init_map_field);
    }).on('change', '.google-map', function() {
        // Изменение карты при изменении координат в текстовом поле
        var $field = $(this);
        var $map = $field.next('div');
        var map_object = $map.data('map');

        // TODO
        var coords = text2coords($field.val());
        map_object.map.panTo(coords);
        map_object.marker.geometry.setCoordinates(coords);
    });

})(jQuery);
