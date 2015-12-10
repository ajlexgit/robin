(function($) {

    /*
        Инспектор, отслеживающий событие, когда элемент находится в поле видимости окна.

        Не следует создавать экземпляры класса VisibilityInspector.
        Следует пользоваться уже созданным экземпляром $.visibilityInspector.

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
        cls.prototype.init = function() {
            this._list = [];
            this.STATE_DATA_KEY = 'visibility_inspector_state';
            this.OPTS_DATA_KEY = 'visibility_inspector_opts';
        };

        cls.prototype.getDefaultOpts = function() {
            return $.extend(superclass.prototype.getDefaultOpts(), {
                top: 1,
                right: 1,
                bottom: 1,
                left: 1
            })
        };

        cls.prototype._check = function($element, opts) {
            var vpWidth = document.documentElement.clientWidth;
            var vpHeight = document.documentElement.clientHeight;
            var rect = $element.get(0).getBoundingClientRect();

            var visible = rect.bottom >= opts.bottom;
            visible = visible && (rect.right >= opts.right);
            visible = visible && ((vpHeight - rect.top) >= opts.top);
            visible = visible && ((vpWidth - rect.left) >= opts.left);

            return visible;
        };

        cls.prototype._afterCheck = function($element, opts, state) {
            var old_state = this.getState($element);
            if (old_state !== state) {
                if (state) {
                    $element.trigger('appear');
                } else {
                    $element.trigger('disappear');
                }
            }

            superclass.prototype._afterCheck.call(this, $element, opts, state);
        };
    });


    // Единственный экземпляр инспектора
    $.visibilityInspector = VisibilityInspector();

    $(window).on('scroll.visibility_inspector', $.rared(function() {
        $.visibilityInspector.checkAll();
    }, 100)).on('resize.visibility_inspector', $.rared(function() {
        $.visibilityInspector.checkAll();
    }, 100));

})(jQuery);