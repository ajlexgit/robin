(function($) {

    /*
        Плагин, имитирующий у блока поведение ссылки.

        Пример:
            <div class="block">
                ...
                <div class="item">
                    <a href="..." class="my-link"></a>
                </div>
                <div class="item">
                    <a href="..." class="my-link"></a>
                </div>
                ...
            </div>


            $('.block').fakeLink({
                itemSelector: '.item',
                linkSelector: '.my-link'
            });
     */

    $.fn.fakeLink = function(options) {
        var settings = $.extend({
            itemSelector: null,
            linkSelector: 'a',
            preventItemClick: true
        }, options);

        var clickHandle = function(event) {
            if (!$(event.target).is(settings.linkSelector)) {
                $(this).find(settings.linkSelector).get(0).click();

                if (settings.preventItemClick) {
                    return false;
                }
            }
        };

        var middleDownHandle = function(event) {
            var targetItem = (event.which === 2) && (!settings.itemSelector || $(this).is(settings.itemSelector));
            return !targetItem;
        };

        var middleUpHandle = function(event) {
            var targetItem = (event.which === 2) && (!settings.itemSelector || $(this).is(settings.itemSelector));
            if (targetItem && !$(event.target).is(settings.linkSelector)) {
                var new_event = new MouseEvent('click', {
                    button: 1
                });

                $(this).find(settings.linkSelector).get(0).dispatchEvent(new_event);
            }
        };

        return this.each(function() {
            var $block = $(this);
            $block.on('click', 'a', function(event) {
                event.stopPropagation();
            });

            if (settings.itemSelector) {
                $block.on('click', settings.itemSelector, clickHandle)
                    .on('mousedown', settings.itemSelector, middleDownHandle)
                    .on('mouseup', settings.itemSelector, middleUpHandle);
            } else {
                $block.on('click', clickHandle)
                    .on('mousedown', middleDownHandle)
                    .on('mouseup', middleUpHandle);
            }
        });
    }

})(jQuery);
