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

    var BackgroundInspector = Class(Inspector, function(cls, superclass) {
        cls.init = function() {
            this._list = [];
            this.STATE_DATA_KEY = 'bginspector_state';
            this.OPTS_DATA_KEY = 'bginspector_opts';
        };


        /*
            Сохраняем inline-стили и сбрасываем размеры
         */
        cls.prototype._beforeCheck = function($element, opts) {
            superclass.prototype._beforeCheck.call(this, $element, opts);
            $element.data('bginspector_inlines', $element.get(0).style.cssText);
            $element.css({
                width: '',
                height: ''
            });
        };

        cls.prototype._check = function($element, opts) {
            var $parent = $element.parent();

            var elem_asp = $element.outerWidth() / $element.outerHeight();
            var parent_asp = $parent.outerWidth() / $parent.outerHeight();
            $element.data('bginspector_aspect', elem_asp);
            $parent.data('bginspector_aspect', parent_asp);

            return elem_asp >= parent_asp;
        };

        /*
            Восстановление inline-стилей
         */
        cls.prototype._afterCheck = function($element, opts, state) {
            $element.get(0).style.cssText = $element.data('bginspector_inlines') || '';
            superclass.prototype._afterCheck.call(this, $element, opts, state);
        };
    });


    // Единственный экземпляр инспектора
    $.bgInspector = BackgroundInspector.create();

    $(window).on('resize.bg_inspector', $.rared(function() {
        $.bgInspector.checkAll();
    }, 60));

})(jQuery);