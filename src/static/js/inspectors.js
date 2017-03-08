(function($) {
    'use strict';

    /*
        Базовый класс инспектирования DOM-элементов.

        Требует:
            jquery.utils.js
     */

    var Inspector = Class(Object, function Inspector(cls, superclass) {
        cls.defaults = {
            checkOnInit: true,
            beforeCheck: $.noop,
            afterCheck: $.noop
        };

        cls.INSPECT_CLASS = '';
        cls.STATE_DATA_KEY = 'inspector_state';
        cls.OPTS_DATA_KEY = 'inspector_opts';

        cls.init = $.noop;

        /*
            Получение настроек DOM-элемента
         */
        cls.getOpts = function($element) {
            return $element.first().data(this.OPTS_DATA_KEY) || this.defaults;
        };

        /*
            Сохранение настроек DOM-элемента
         */
        cls._setOpts = function($element, opts) {
            $element.first().data(this.OPTS_DATA_KEY, opts).addClass(this.INSPECT_CLASS);
        };

        /*
            Получение состояния DOM-элемента
         */
        cls.getState = function($element) {
            return $element.first().data(this.STATE_DATA_KEY);
        };

        /*
            Сохранение состояния DOM-элемента
         */
        cls._setState = function($element, state) {
            $element.first().data(this.STATE_DATA_KEY, state);
        };


        // ================================================================

        cls._beforeCheck = function($element, opts) {
            opts.beforeCheck.call(this, $element, opts);
        };

        cls._check = function($element, opts) {
            throw Error('not implemented');
        };

        cls._afterCheck = function($element, opts, state) {
            opts.afterCheck.call(this, $element, opts, state);
            this._setState($element, state);
        };

        // ================================================================

        /*
            Функция, проверяющая условие инспектирования на элементах или селекторе
         */
        cls.check = function(elements, options) {
            var that = this;

            var $elements = $(elements);
            $elements.each(function(i, elem) {
                var $elem = $(elem);

                var opts = $.extend({}, that.getOpts($elem), options);
                if (!opts) {
                    that.error('checking options required');
                    return;
                }

                that._beforeCheck($elem, opts);
                var state = that._check($elem, opts);
                that._afterCheck($elem, opts, state);
            });
        };

        /*
            Добавление селекора элементов для инспектирования
         */
        cls.inspect = function(selector, options) {
            var opts = $.extend({}, this.defaults, options);
            if (!opts) {
                return this.error('inspecting options required');
            }

            var that = this;
            var $elements = $(selector);

            // если селектор уже инспектируется - удаляем его
            this.ignore(selector);

            // инициализация состояния элементов
            $elements.each(function(i, elem) {
                var $elem = $(elem);
                that._setOpts($elem, opts);
                that._setState($elem, null);

                // сразу проверяем элементы
                if (opts.checkOnInit) {
                    that.check($elem);
                }
            });

            return $elements;
        };

        /*
            Удаление селектора из инспектирования
         */
        cls.ignore = function(selector) {
            var that = this;
            $(selector).removeClass(this.INSPECT_CLASS).each(function(i, elem) {
                var $elem = $(elem);
                $elem.removeData(that.OPTS_DATA_KEY + ' ' + that.STATE_DATA_KEY);
            });
        };

        /*
            Проверка всех инспектируемых элементов
         */
        cls.checkAll = function() {
            this.check('.' + this.INSPECT_CLASS);
        };
    });


    /*
        Инспектор, отслеживающий событие, когда ширина окна превысила
        некоторый лимит, либо опустилась ниже него.

        Не следует создавать экземпляры класса MediaInspector.
        Следует пользоваться уже созданным экземпляром $.mediaInspector.

        Требует:
            jquery.utils.js

        Параметры:
            point: int  - breakpoint

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

        cls.INSPECT_CLASS = 'media-inspect';
        cls.STATE_DATA_KEY = 'media_inspector_state';
        cls.OPTS_DATA_KEY = 'media_inspector_opts';

        cls._check = function($element, opts) {
            return $.winWidth() >= opts.point;
        };
    });

    // Единственный экземпляр инспектора
    $.mediaInspector = MediaInspector();


    /*
        Инспектор, отслеживающий изменение аспекта картинки по отношению к
        аспекту родительского элемента.

        Не следует создавать экземпляры класса BackgroundInspector.
        Следует пользоваться уже созданным экземпляром $.bgInspector.

        Требует:
            jquery.utils.js

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

        cls.INSPECT_CLASS = 'bg-inspect';
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
                    if ($element.prop('naturalWidth')) {
                        that.check(this);
                    }
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


    /*
        Инспектор, отслеживающий событие, когда элемент находится в поле видимости окна.

        Не следует создавать экземпляры класса VisibilityInspector.
        Следует пользоваться уже созданным экземпляром $.visibilityInspector.

        Возбуждает события appear / disappear на инспектируемых элементах.

        Требует:
            jquery.utils.js

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

            var invisible_by_top = (rect.top > (vpHeight - opts.top));
            var invisible_by_bottom = (rect.bottom < opts.bottom);
            var invisible_by_left = (rect.left > (vpWidth - opts.left));
            var invisible_by_right = (rect.right < opts.right);

            return !invisible_by_top && !invisible_by_bottom && !invisible_by_left && !invisible_by_right;
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
    }, 100)).on('resize.inspector', $.rared(function() {
        $.mediaInspector.checkAll();
        $.visibilityInspector.checkAll();
        $.bgInspector.checkAll();
    }, 60)).on('load.inspector', function() {
        $.mediaInspector.checkAll();
        $.visibilityInspector.checkAll();
        $.bgInspector.checkAll();
    });

})(jQuery);