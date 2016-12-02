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

        Пример с плейсхолдером:
            <div data-src="read-image.jpg" class="lazyload onview"></div>

     */

    var DATA_TO_ATTRS = ['src', 'srcset', 'sizes', 'alt', 'width', 'height'];

    $.fn.loadImage = function() {
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

            if (this.tagName == 'IMG') {
                $this.attr(attrs).addClass('loaded').removeClass('lazyload');
                return this;
            } else {
                var $img = $('<img/>');
                $img.onLoaded(function() {
                    $this.before($img).remove();
                    $img.addClass('loaded').removeClass('lazyload');
                });
                $img.attr(attrs).addClass($this.attr('class'));
                return $img;
            }
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
