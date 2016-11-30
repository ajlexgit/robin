(function($) {

    /*
        Отложенная загрузка картинок.
        Необходимо добавить тэгу img класс "lazyload" и перенести атрибуты src/srcset/sizes в data.

        Требует:
            visibility_inspector.js

        Дополнительные классы:
            onview      - загрузка, когда элемент станет видимым

        Принудительно начать загрузку:
            $('.lazyload').loadImage();

        Пример:
            <img src="blank.gif" data-src="read-image.jpg" alt="..." class="lazyload onview">

     */

    $.fn.loadImage = function() {
        return this.each(function() {
            var $img = $(this);
            var img_data = $img.data();
            var attrs = {};

            if (img_data.src) {
                attrs.src = img_data.src;
            }
            if (img_data.srcset) {
                attrs.srcset = img_data.srcset;
            }
            if (img_data.sizes) {
                attrs.sizes = img_data.sizes;
            }

            $img.attr(attrs).addClass('loaded').removeClass('lazyload');
        });
    };

    $(document).ready(function() {
        var $images = $('.lazyload');

        if ($.visibilityInspector) {
            $.visibilityInspector.inspect($images.filter('.onview'), {
                afterCheck: function($elem, opts, state) {
                    if (state) {
                        $elem.loadImage();
                    }
                }
            });
        }
    });

})(jQuery);
