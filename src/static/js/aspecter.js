(function($) {

    /*
        Регистратор обработчиков, выполняющихся когда изменяется
        отношение аспекта блока и его родителя (когда блок по пропорциям
        шире, чем его родитель).

        Требует:
            jquery.utils.js

        Параметры:
            beforeCheck - функция, вызываемая до проверки
            afterCheck  - функция, вызываемая после проверки

        Пример:
            $('.block').inspect_aspecter().on('wider', function() {
                console.log('block is wider than parent');
            }).on('higher', function() {
                console.log('block is higher than parent');
            });

            // удаление элементов из инспектирования
            $('.block').ignore_aspecter()

            // Проверка пропорций ПЕРВОГО найденого элемента
            $('.block').is_wider({
                beforeCheck: function() {
                    $(this).width('');
                }
            })
     */

    window.Aspecter = Class(null, function(cls, superclass) {
        var inspected = [];

        // параметры по умолчанию
        var default_opts = {
            beforeCheck: $.noop,
            afterCheck: $.noop
        };

        // удаление элемента из инспектирования, если он есть
        var unregister_element = function(elem) {
            var index = inspected.indexOf(elem);
            if (index >= 0) {
                delete elem._aspecter_state;
                delete elem._aspecter_opts;
                inspected.splice(index, 1);
            }
        };

        cls.init = function() {
            // запрещено создавать экземпляры
            console.error('Aspecter: creating instances are disallowed');
            return false;
        };

        /*
            Определение состояния видимости элемента.
            Если передан селектор - будет проверен первый найденный элемент
         */
        cls.is_wider = function(element, options) {
            var $element = $(element);
            if (!$element.length) {
                console.error('Aspecter: not found element for checking');
                return false;
            }

            element = $element[0];
            if (!element || !element.nodeType ||
                (element.nodeType != 1)) {
                console.error('Aspecter: bad element ' + element);
            }

            var opts = options || element._aspecter_opts || default_opts;
            opts.beforeCheck.call(element);

            var elem_rect = element.getBoundingClientRect();
            var parent_rect = element.parentNode.getBoundingClientRect();
            var wider = (elem_rect.width / elem_rect.height) >= (parent_rect.width / parent_rect.height);

            opts.afterCheck.call(element);
            return wider;
        };

        /*
            Добавление элементов для инспектирования изменения их пропорций
         */
        cls.inspect = function(elements, options) {
            var $elements = $(elements);
            if (!$elements.length) {
                console.error('Aspecter: "inspect" method requires elements');
                return;
            }

            // настройки
            var opts = $.extend({}, default_opts, options);

            $elements.each(function(i, elem) {
                // если элемент уже испектируется - удаляем его
                unregister_element(elem);

                // инициализация состояния
                elem._aspecter_state = cls.is_wider(elem, opts);
                elem._aspecter_opts = opts;

                inspected.push(elem);
            });
        };

        /*
            Удаление элементов из инспектирования.
         */
        cls.ignore = function(elements) {
            var $elements = $(elements);
            if (!$elements.length) {
                console.error('Aspecter: "ignore" method requires elements');
                return;
            }

            $elements.each(function(i, elem) {
                unregister_element(elem);
            });
        };

        /*
            Проверка элемента и вызов событий на нем,
            если его состояние пропорций изменилось.
         */
        cls.check = function(element, force) {
            var old_state = element._aspecter_state;
            if (old_state === undefined) {
                return;
            }

            var new_state = this.is_wider(element, element._aspecter_opts);
            if (force || (new_state != old_state)) {
                element._aspecter_state = new_state;
                if (new_state) {
                    $(element).trigger('wider');
                } else {
                    $(element).trigger('higher');
                }
            }
        };

        /*
            Проверка всех инспектируемых элементов и вызов событий на них,
            если их состояние пропорций изменилось.
         */
        cls.check_inspected = function() {
            for (var i = 0, l = inspected.length; i < l; i++) {
                cls.check(inspected[i]);
            }
        }
    });

    // Алиас для Aspecter.check
    $.fn.check_aspecter = function(force) {
        return this.each(function(i, elem) {
            Aspecter.check(elem, force);
        });
    };

    // Алиас для Aspecter.inspect
    $.fn.inspect_aspecter = function(options) {
        Aspecter.inspect(this, options);
        return this;
    };

    // Алиас для Aspecter.ignore
    $.fn.ignore_aspecter = function() {
        Aspecter.ignore(this);
        return this;
    };

    // Алиас для Aspecter.is_wider
    $.fn.is_wider = function(options) {
        return Aspecter.is_wider(this, options);
    };

    var check_inspected_handler = function() {
        Aspecter.check_inspected();
    };

    $(document).ready(function() {
        setTimeout(check_inspected_handler, 0);
    });

    $(window).on('resize.aspecter', $.rared(check_inspected_handler, 100));

})(jQuery);