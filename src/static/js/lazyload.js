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
            <img data-src="read-image.jpg" class="lazyload onview">

        Примеры с плейсхолдером:
            // simple
            <div data-src="read-image.jpg" class="lazyload onview"></div>

            // extended
            <div class="lazyload" style="width: {{ image.width }}px" data-src="{{ image.url }}">
              <div style="padding-bottom: {{ image.space }}"></div>
            </div>
            <noscript>
              <img src="{{ image.url }}" alt="">
            </noscript>

     */

    var DATA_TO_ATTRS = ['src', 'srcset', 'sizes', 'alt', 'width', 'height'];

    $.fn.loadImage = function(callback) {
        return this.map(function() {
            var $this = $(this);
            var this_data = $this.data();

            // защита от вызова для посторонних элементов
            if (!$this.hasClass('lazyload')) {
                return this;
            }

            // аттрибуты из data-параметров
            var attrs = {};
            for (var i=0, l=DATA_TO_ATTRS.length; i<l; i++) {
                var property = DATA_TO_ATTRS[i];
                if (this_data[property]) {
                    attrs[property] = this_data[property];
                }
            }


            var $img = $('<img/>', {alt: ''});
            $img.onLoaded(function() {
                $this.before($img).remove();
                $img.addClass('loaded').removeClass('lazyload');

                if ($.isFunction(callback)) {
                    callback.call($img.get(0));
                }
            });

            $img.attr(attrs).addClass($this.attr('class'));
            return $img;
        });
    };

    $(document).ready(function() {
        var $images = $('.lazyload');

        if ($.visibilityInspector) {
            $.visibilityInspector.inspect($images.filter('.onview'), {
                afterCheck: function($elem, opts, state) {
                    if (state) {
                        $elem.loadImage();
                        this.ignore($elem);
                    }
                }
            });
        }
    });

})(jQuery);
