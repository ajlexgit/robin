(function($) {
    'use strict';

    /*
        Инспектор, отслеживающий событие, когда ширина окна превысила
        некоторый лимит, либо опустилась ниже него.

        Не следует создавать экземпляры класса MediaInspector.
        Следует пользоваться уже созданным экземпляром $.mediaInspector.

        В качестве state возвращается наибольший из breakpoint-ов:
        Например, при point = [768, 1024, 1200], с шириной экрана 1100,
        будет возвращено 1024. Если все числа в массиве меньше ширины экрана,
        в state будет ноль.

        Требует:
            jquery.utils.js, inspector.js

        Параметры:
            point: int / array      - breakpoint или массив breakpoint'ов

        Пример:
            $.mediaInspector.inspect('body', {
                point: 768,
                afterCheck: function($elem, opts, state) {
                    if (state) {
                        console.log('Ширина экрана >= 768');
                    } else {
                        console.log('Ширина экрана < 768');
                    }
                }
            });

            // немедленная проверка элемента
            $.mediaInspector.check('body');

            // удаление элементов из инспектирования
            $.mediaInspector.ignore('body');
     */

    var MediaInspector = Class(Inspector, function MediaInspector(cls, superclass) {
        cls.defaults = $.extend({}, superclass.defaults, {
            point: 0
        });

        cls.STATE_DATA_KEY = 'media_inspector_state';
        cls.OPTS_DATA_KEY = 'media_inspector_opts';


        cls._check = function($element, opts) {
            var state = 0;
            var winWidth = $.winWidth();
            if ($.isArray(opts.point)) {
                opts.point.forEach(function(point) {
                    if (winWidth >= point) {
                        state = Math.max(state, point);
                    }
                })
            } else {
                state = winWidth >= opts.point;
            }

            return state;
        };
    });


    // Единственный экземпляр инспектора
    $.mediaInspector = MediaInspector();

    $(window).on('resize.media_inspector', $.rared(function() {
        $.mediaInspector.checkAll();
    }, 100));

})(jQuery);