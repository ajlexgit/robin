(function($) {

    if (!window.boxberry) {
        window.boxberry = {};
    }

    /*
        Получение городов
     */
    window.boxberry.getCities = function() {
        return $.ajax({
            url: window.js_storage.boxberry_cities_url,
            dataType: 'json'
        })
    };

    /*
        Получение пунктов выдачи в заданном городе (56 - Тольятти)
     */
    window.boxberry.getPoints = function(city_id) {
        return $.ajax({
            url: window.js_storage.boxberry_points_url.replace(/0/i, city_id),
            dataType: 'json'
        })
    };

    /*
        Получение информации о пункте выдачи (214 - Ленина 19)
     */
    window.boxberry.getPoint = function(point_id, photos) {
        photos = Number(Boolean(photos));
        return $.ajax({
            url: window.js_storage.boxberry_point_url.replace(/0/i, point_id)+'?photos='+photos,
            dataType: 'json'
        })
    };

    /*
        Получение стоимости доставки в заданный пукнт выдачи
     */
    window.boxberry.getCost = function(point_id, options) {
        var query = $.map(options, function(value, key) {
            return key + '=' + encodeURIComponent(value);
        }).join('&');

        return $.ajax({
            url: window.js_storage.boxberry_cost_url.replace(/0/i, point_id) + '?' + query,
            dataType: 'json'
        })
    };

})(jQuery);