(function($) {

    /*
        Инспектор, отслеживающий изменение аспекта картинки по отношению к
        аспекту родительского элемента.

        Не следует создавать экземпляры класса BackgroundInspector.
        Следует пользоваться уже созданным экземпляром $.bgInspector.

        Требует:
            jquery.utils.js, inspector.js

        Пример:
            $.bgInspector.inspect('.parallax', {
                afterCheck: function($elem, opts, state) {
                    if (state) {
                        console.log('Картинка пропорционально шире, чем родительский элемент');
                    } else {
                        console.log('Картинка пропорционально выше, чем родительский элемент');
                    }
                }
            });

            // немедленная проверка элемента
            $.bgInspector.check('.parallax');

            // удаление элементов из инспектирования
            $.bgInspector.ignore('.parallax');
     */

    var BackgroundInspector = Class(Inspector, function BackgroundInspector(cls, superclass) {
        cls.defaults = $.extend({}, superclass.defaults, {
            getContainer: function($element) {
                return $element.parent();
            },
            afterCheck: function($elem, opts, state) {
                if (state) {
                    $elem.css({
                        width: 'auto',
                        height: '100.6%'
                    });
                } else {
                    $elem.css({
                        width: '100.6%',
                        height: 'auto'
                    });
                }
            }
        });

        cls.STATE_DATA_KEY = 'bg_inspector_state';
        cls.OPTS_DATA_KEY = 'bg_inspector_opts';


        /*
            Сохраняем inline-стили и сбрасываем размеры
         */
        cls._beforeCheck = function($element, opts) {
            superclass._beforeCheck.call(this, $element, opts);
            $element.data('bginspector_inlines', $element.get(0).style.cssText);
            $element.css({
                width: '',
                height: ''
            });
        };

        cls._check = function($element, opts) {
            // если проверяется картинка и она еще не загружена,
            // повторяем проверку после загрузки.
            if (($element.prop('tagName') == 'IMG') && !$element.prop('naturalWidth')) {
                var that = this;
                $element.onLoaded(function() {
                    that.check($element);
                });
            }

            var $parent = opts.getContainer.call(this, $element);
            var elem_asp = $element.outerWidth() / $element.outerHeight();
            var parent_asp = $parent.outerWidth() / $parent.outerHeight();
            $element.data('bginspector_aspect', elem_asp);
            $parent.data('bginspector_aspect', parent_asp);
            return elem_asp >= parent_asp;
        };

        /*
            Восстановление inline-стилей
         */
        cls._afterCheck = function($element, opts, state) {
            $element.get(0).style.cssText = $element.data('bginspector_inlines') || '';
            superclass._afterCheck.call(this, $element, opts, state);
        };
    });


    // Единственный экземпляр инспектора
    $.bgInspector = BackgroundInspector();

    $(window).on('resize.bg_inspector', $.rared(function() {
        $.bgInspector.checkAll();
    }, 60));

})(jQuery);