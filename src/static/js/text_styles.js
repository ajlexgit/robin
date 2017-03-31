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
        // оборачивание таблиц
        $('.text-styles table').each(function() {
            $(this).wrap(
                $('<div/>').addClass('page-table')
            )
        });

        // замена описаний на тег span
        $('.page-video, .single-image').each(function() {
            var $block = $(this);
            var $image = $block.find('img').first();
            var description = cut_description(this) || $.trim(atob($image.data('description') || ''));
            if (description) {
                $block.append(
                    $('<div>').addClass('object-description').html(description.replace(/[\n\r]+/g, '<br>'))
                )
            }
        });

        // Слайдеры с описанием
        $('.page-images.multi-image').each(function() {
            var description = cut_description(this);
            $(this).find('img').wrap('<div class="slider-item"/>').each(function() {
                var $image = $(this);
                var description = $.trim(atob($image.data('description') || ''));
                if (description) {
                    $image.after(
                        $('<div>').addClass('item-description').html(description.replace(/[\n\r]+/g, '<br>'))
                    );
                }
            });

            var slider = Slider(this, {
                sliderHeight: Slider.prototype.HEIGHT_CURRENT
            }).attachPlugins([
                SliderSideAnimation({}),
                SliderSideShortestAnimation({}),
                SliderControlsPlugin({
                    animationName: 'side-shortest'
                }),
                SliderDragPlugin({})
            ]);

            slider.$root.on('click', '.slider-item', function() {
                slider.slideNext('side-shortest', true);
            });

            // вставляем описание в слайдер
            if (description) {
                slider.$root.append(
                    $('<div>').addClass('object-description').html(description)
                )
            }
        });

        // Видео на всю ширину с сохранением пропорций
        $('.page-video').fitVids();
    });

})(jQuery);
