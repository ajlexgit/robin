(function($) {
    'use strict';

    /*
        Требует:
            jquery.fitvids.js, slider.js
    */

    var cut_description = function(element) {
        var i = 0;
        var child;
        var description = '';
        var childs = element.childNodes;
        while (child = childs[i]) {
            if (child.nodeType == 3) {
                description += child.data;
                element.removeChild(child);
            } else if (child.tagName == 'BR') {
                if (description) {
                    // пропускаем первые BR
                    description += child.outerHTML;
                }
                element.removeChild(child);
            } else if (child.tagName == 'SPAN') {
                var text = cut_description(child);
                if (text) {
                    description += text;
                }
                element.removeChild(child);
            } else {
                i++
            }
        }

        return $.trim(description);
    };

    $(document).ready(function() {
        // замена описаний на тег span
        $('.page-video, .single-image').each(function() {
            var description = cut_description(this);
            if (description) {
                $(this).append(
                    $('<div>').addClass('object-description').html(description)
                )
            }
        });

        // Слайдеры с описанием
        $('.page-images.multi-image').each(function() {
            var description = cut_description(this);

            var slider = Slider(this, {
                itemSelector: 'img'
            }).attachPlugins([
                SliderSideAnimation({}),
                SliderSideShortestAnimation({}),
                SliderControlsPlugin({
                    animationName: 'side-shortest'
                }),
                SliderDragPlugin({})
            ]);

            // вставляем описание в слайдер
            if (description) {
                slider.$root.append(
                    $('<div>').addClass('description').html(description)
                )
            }
        });

        // Видео на всю ширину с сохранением пропорций
        $('.page-video').fitVids();
    });

})(jQuery);
