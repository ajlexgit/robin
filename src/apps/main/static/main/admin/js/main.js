(function() {

    $(document).on('change', '#id_address', function() {
        var ymap_object = $('#id_coords').next('div').data('map');
        ymap_object.addressCoords($(this).val());

        var gmap_object = $('#id_coords2').next('div').data('map');
        gmap_object.addressCoords($(this).val());
    });

})(jQuery);