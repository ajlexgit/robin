(function($) {

    /*
        Добавляет события появления/исчезновения элемента из
        поля видимости.

        Учитывает display:none, но не учитывает visible:hidden.

        Требует:
            jquery.utils.js

        Параметры:
            расстояние от соответствующей границы элемента до
            соответствующей границы окна браузера,
            при превышении которого элемент считается видимым/невидимым.

            beforeCheck - функция, вызываемая до проверки
            afterCheck  - функция, вызываемая после проверки

        Пример:
            $('.block').inspect_visibility().on('appear', function() {
                console.log('block became visible');
            }).on('dissapear', function() {
                console.log('block became invisible');
            });

            // удаление элементов из инспектирования
            $('.block').ignore_visibility()

            // Проверка видимости ПЕРВОГО найденого элемента
            $('.block').is_visible({
                top: 50,
                bottom: 50
            })
     */

    window.Visibility = Class(null, function(cls, superclass) {
        var inspected = [];

        // параметры по умолчанию
        var default_opts = {
            top: 1,
            right: 1,
            bottom: 1,
            left: 1,
            beforeCheck: $.noop,
            afterCheck: $.noop
        };

        // удаление элемента из инспектирования, если он есть
        var unregister_element = function(elem) {
            var index = inspected.indexOf(elem);
            if (index >= 0) {
                $(elem).removeData('appear_state appear_opts');
                inspected.splice(index, 1);
            }
        };

        cls.init = function() {
            // запрещено создавать экземпляры
            console.error('Visibility: creating instances are disallowed');
            return false;
        };

        /*
            Определение состояния видимости элемента.
            Если передан селектор - будет проверен первый найденный элемент
         */
        cls.is_visible = function(element, options) {
            var $element = $(element).first();
            if (!$element.length) {
                console.error('Visibility: not found element for checking');
                return false;
            }

            element = $element[0];
            if (!element || !element.nodeType ||
                (element.nodeType != 1)) {
                console.error('Visibility: bad element ' + element);
            }

            var elem_data = $element.data();
            var opts = options || elem_data.appear_opts || default_opts;

            // callback
            opts.beforeCheck.call(element);

            var vpWidth = document.documentElement.clientWidth;
            var vpHeight = document.documentElement.clientHeight;
            var rect = element.getBoundingClientRect();
            var visible = rect.bottom >= opts.bottom;
            visible = visible && (rect.right >= opts.right);
            visible = visible && ((vpHeight - rect.top) >= opts.top);
            visible = visible && ((vpWidth - rect.left) >= opts.left);

            // callback
            opts.afterCheck.call(element);

            return visible;
        };

        /*
            Добавление элементов для инспектирования их
            появления и исчезновения из области видимости.
         */
        cls.inspect = function(elements, options) {
            var $elements = $(elements);
            if (!$elements.length) {
                console.error('Visibility: "inspect" method requires elements');
                return;
            }

            // настройки
            var opts = $.extend({}, default_opts, options);

            $elements.each(function(i, elem) {
                // если элемент уже испектируется - удаляем его
                unregister_element(elem);

                // инициализация состояния видимости
                $(elem).data({
                    appear_state: cls.is_visible(elem, opts),
                    appear_opts: opts
                });

                inspected.push(elem);
            });
        };

        /*
            Удаление элементов из инспектирования.
         */
        cls.ignore = function(elements) {
            var $elements = $(elements);
            if (!$elements.length) {
                console.error('Visibility: "ignore" method requires elements');
                return;
            }

            $elements.each(function(i, elem) {
                unregister_element(elem);
            });
        };

        /*
            Проверка элемента и вызов событий на нем,
            если его состояние видимости изменилось.
         */
        cls.check = function(element) {
            var $element = $(element).first();
            if (!$element.length) {
                console.error('Visibility: not found element for checking');
                return;
            }

            var elem_data = $element.data();
            var old_state = elem_data.appear_state;
            if (old_state === undefined) {
                return;
            }

            var new_state = this.is_visible(element, elem_data.appear_opts);
            if (new_state != old_state) {
                elem_data.appear_state = new_state;
                if (new_state) {
                    $(element).trigger('appear');
                } else {
                    $(element).trigger('disappear');
                }
            }
        };

        /*
            Проверка всех инспектируемых элементов и вызов событий на них,
            если их состояние видимости изменилось.
         */
        cls.check_inspected = function() {
            for (var i = 0, l = inspected.length; i < l; i++) {
                cls.check(inspected[i]);
            }
        }
    });

    // Алиас для Visibility.check
    $.fn.check_visibility = function() {
        return this.each(function(i, elem) {
            Visibility.check(elem);
        });
    };

    // Алиас для Visibility.inspect
    $.fn.inspect_visibility = function(options) {
        Visibility.inspect(this, options);
        return this;
    };

    // Алиас для Visibility.ignore
    $.fn.ignore_visibility = function() {
        Visibility.ignore(this);
        return this;
    };

    // Алиас для Visibility.is_visible
    $.fn.is_visible = function(options) {
        return Visibility.is_visible(this, options);
    };


    var check_inspected_handler = function() {
        Visibility.check_inspected();
    };

    $(document).ready(function() {
        setTimeout(check_inspected_handler, 0);
    });

    $(window)
        .on('scroll.appear resize.appear', $.rared(check_inspected_handler, 100))
        .on('load.appear', check_inspected_handler);

})(jQuery);
