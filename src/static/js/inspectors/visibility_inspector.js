(function($) {
    'use strict';

    /*
        Инспектор, отслеживающий событие, когда элемент находится в поле видимости окна.

        Не следует создавать экземпляры класса VisibilityInspector.
        Следует пользоваться уже созданным экземпляром $.visibilityInspector.

        Возбуждает события appear / disappear на инспектируемых элементах.

        Требует:
            jquery.utils.js, inspector.js

        Параметры:
            расстояние от соответствующей границы элемента до
            соответствующей границы окна браузера,
            при превышении которого элемент считается видимым/невидимым.

            beforeCheck - функция, вызываемая до проверки
            afterCheck  - функция, вызываемая после проверки

        Пример:
            $.visibilityInspector.inspect('.block', {
                top: 20,
                bottom: 20,
                afterCheck: function($elem, opts, state) {
                    if (state) {
                        console.log('Элемент виден минимум на 20px');
                    } else {
                        console.log('Элемент виден менее, чем на 20px');
                    }
                }
            });

            // немедленная проверка элемента
            $.visibilityInspector.check('.block');

            // удаление элементов из инспектирования
            $.visibilityInspector.ignore('.block');
     */

    var VisibilityInspector = Class(Inspector, function VisibilityInspector(cls, superclass) {
        cls.defaults = $.extend({}, superclass.defaults, {
            top: 1,
            right: 1,
            bottom: 1,
            left: 1
        });

        cls.INSPECT_CLASS = 'visbility-inspect';
        cls.STATE_DATA_KEY = 'visibility_inspector_state';
        cls.OPTS_DATA_KEY = 'visibility_inspector_opts';


        cls._check = function($element, opts) {
            var vpWidth = $.winWidth();
            var vpHeight = $.winHeight();
            var rect = $element.get(0).getBoundingClientRect();

            var from_top = (rect.top >= 0) && ((vpHeight - rect.top) >= opts.top);
            var from_bottom = (rect.bottom >= opts.bottom) && (rect.bottom <= vpHeight);
            var from_left = (rect.left >= 0) && ((vpWidth - rect.left) >= opts.left);
            var from_right = (rect.right >= opts.right) && (rect.right <= vpWidth);

            return (from_top || from_bottom) && (from_left || from_right);
        };

        cls._afterCheck = function($element, opts, state) {
            var old_state = this.getState($element);
            if (old_state !== state) {
                if (state) {
                    $element.trigger('appear');
                } else {
                    $element.trigger('disappear');
                }
            }

            superclass._afterCheck.call(this, $element, opts, state);
        };
    });


    // Единственный экземпляр инспектора
    $.visibilityInspector = VisibilityInspector();

    $(window).on('scroll.visibility_inspector', $.rared(function() {
        $.visibilityInspector.checkAll();
    }, 100)).on('resize.visibility_inspector', $.rared(function() {
        $.visibilityInspector.checkAll();
    }, 100)).on('load.visibility_inspector', function() {
        $.visibilityInspector.checkAll();
    });

})(jQuery);