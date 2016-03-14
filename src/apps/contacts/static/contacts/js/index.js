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
            }

            $address.addClass('active').siblings().removeClass('active');
        }
    });

    $(document).ready(function() {
        var $addresses = $('#google-map').find('.address');
        if ($addresses.length) {
            var $first = $addresses.first();

            gmap = GMap('#google-map .map', {
                center: pointByAddr($first),
                zoom: 14
            }).on('ready', function() {
                GMapMarker({
                    map: this,
                    position: this.center()
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


    // Форма контактов
    $(document).on('submit', '#contact-form', function() {
        var preloader = $.preloader();

        // Добавляем адрес страницы, с которой отправили сообщение
        var $form = $(this);
        var data = $form.serializeArray();
        data.push({
            name: 'referer',
            value: location.href
        });

        $.ajax({
            url: window.js_storage.ajax_contact,
            type: 'POST',
            data: data,
            dataType: 'json',
            beforeSend: function() {
                // сброс ошибок формы
                $form.find('.errors').each(function() {
                    this.className = this.className.replace(/\berror.*?\b/g, '');
                });
            },
            success: function(response) {
                if (response.success_message) {
                    // сообщение о успешной отправке
                    $.popup({
                        classes: 'contact-popup contact-success-popup',
                        content: response.success_message
                    }).show();

                    $form.get(0).reset();
                } else {
                    preloader.destroy();
                }
            },
            error: $.parseError(function(response) {
                preloader.destroy();
                if (response && response.errors) {
                    // ошибки формы
                    var first_error;

                    response.errors.forEach(function(record) {
                        var $field = $form.find('.field-' + record.field);
                        if ($field.length) {
                            if (!first_error) {
                                first_error = $field.get(0);
                            }
                            $field.addClass(record.classes);
                        }
                    });

                    if (first_error) {
                        $.scrollTo(first_error, 400, {
                            offset: {
                                top: -20
                            }
                        });
                    }
                } else {
                    alert(window.DEFAULT_AJAX_ERROR);
                }
            })
        });
        return false;
    });

})(jQuery);
