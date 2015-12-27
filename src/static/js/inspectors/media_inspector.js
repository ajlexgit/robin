(function($) {

    /*
        Инспектор, отслеживающий событие, когда ширина окна превысила
        некоторый лимит, либо опустилась ниже него.

        Не следует создавать экземпляры класса MediaInspector.
        Следует пользоваться уже созданным экземпляром $.mediaInspector.

        Требует:
            jquery.utils.js, inspector.js

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
            return window.innerWidth >= opts.point;
        };
    });


    // Единственный экземпляр инспектора
    $.mediaInspector = MediaInspector();

    $(window).on('resize.media_inspector', $.rared(function() {
        $.mediaInspector.checkAll();
    }, 100));

})(jQuery);