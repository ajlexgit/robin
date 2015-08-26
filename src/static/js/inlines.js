(function($) {

    /*
        Плагин для работы с inline-формами на клиенте.

        Требует:
            jquery.utils.js

        Пример HTML:
            <div id="formset">
                {{ formset.management_form }}

                <div class="forms">
                  {% for form in formset %}
                    <div class="form">
                      {{ form }}
                    </div>
                  {% endfor %}
                </div>

                <div class="form empty-form">
                   {% with form=formset.empty_form %}
                       {{ form }}
                  {% endwith %}
                </div>
            </div>

     */

    var prefix_regexp = /__prefix__/i;
    var setElementIndex = function(element, index) {
        // label tag
        var for_value = element.getAttribute('for');
        if (for_value) {
            element.setAttribute('for', for_value.replace(prefix_regexp, index));
        }

        // ID attr
        if (element.id) {
            element.id = element.id.replace(prefix_regexp, index);
        }

        // name attr
        if (element.name) {
            element.name = element.name.replace(prefix_regexp, index);
        }
    };

    window.Formset = (function() {
        var Formset = function(root, settings) {
            var $root = $(root).first();
            if (!$root.length) {
                console.error('Empty root element for Formset');
                return
            } else {
                this.$root = $root;
            }

            this.opts = $.extend(true, this.getDefaultOpts(), settings);

            // mangement form
            this.management = this.getManagementForm();

            // forms container
            this.$container = this.getFormsContainer();

            // Находим формы, которые уже есть
            var $initial_forms = this.getForms();

            // индекс следующей добавленной формы
            this.nextFormIndex = $initial_forms.length;

            // Помечаем реально начальные формы
            var initial_count = parseInt(this.management.$initial_forms.val());
            if ($initial_forms.length < initial_count) {
                console.error('INITIAL_FORMS is less than real from count');
                return
            }
            $initial_forms.slice(0, initial_count).data('initial', true);
        };

        /*
            Настройки по умолчанию
         */
        Formset.prototype.getDefaultOpts = function() {
            return {
                formsContainerClass: 'forms',
                emptyFormClass: 'empty-form',
                formClass: 'form',

                prefix: 'form',
                pkFieldName: 'id'
            }
        };

        /*
            Получение полей management-формы
         */
        Formset.prototype.getManagementForm = function() {
            var $total_forms = $('#id_' + this.opts.prefix + '-TOTAL_FORMS');
            var $initial_forms = $('#id_' + this.opts.prefix + '-INITIAL_FORMS');
            var $min_num_forms = $('#id_' + this.opts.prefix + '-MIN_NUM_FORMS');
            var $max_num_forms = $('#id_' + this.opts.prefix + '-MAX_NUM_FORMS');

            if (!$total_forms.length) {
                console.error('Not found TOTAL_FORMS field');
            }
            if (!$initial_forms.length) {
                console.error('Not found INITIAL_FORMS field');
            }
            if (!$min_num_forms.length) {
                console.error('Not found MIN_NUM_FORMS field');
            }
            if (!$max_num_forms.length) {
                console.error('Not found MAX_NUM_FORMS field');
            }

            return {
                $total_forms: $total_forms,
                $initial_forms: $initial_forms,
                $min_num_forms: $min_num_forms,
                $max_num_forms: $max_num_forms
            }
        };

        /*
            Получение всех форм набора
         */
        Formset.prototype.getFormsContainer = function() {
            return this.$root.find('.' + this.opts.formsContainerClass);
        };

        /*
            Получение всех форм набора
         */
        Formset.prototype.getForms = function() {
            return this.$container.find('.' + this.opts.formClass);
        };


        /*
            Удаление формы. Устанавливает флаг DELETE, если он есть.
            Если форма не была сохранена в БД, уменьшает TOTAL_FORMS.

            Должен вызывать beforeDeleteForm и
         */
        Formset.prototype.deleteForm = function($form) {
            if (this.beforeDeleteForm($form) === false) {
                return
            }

            var form_data = $form.data();
            if (form_data.initial) {
                this.markFormDeleted($form);
                this.hideForm($form);
            } else {
                this.hideForm($form, true);
            }
        };

        Formset.prototype.beforeDeleteForm = function($form) {
            // jQuery event
            this.$container.trigger('beforeDeleteForm.formset', [$form]);
        };

        Formset.prototype.afterDeleteForm = function($form) {
            // jQuery event
            this.$container.trigger('afterDeleteForm.formset', [$form]);
        };

        /*
            Отметка initial-формы, что она должна быть удалена
         */
        Formset.prototype.markFormDeleted = function($form) {
            var id_prefix = 'id_' + this.opts.prefix + '-';
            var $delete_field = $form.find('[id^="' + id_prefix + '"][id$="-DELETE"]').first();
            $delete_field.prop('checked', true).val('1').change();
        };

        /*
            Скрытие формы. Если установлен флаг remove - после
            скрытия форма должна быть удалена из DOM.

            Должен вызывать afterDeleteForm.
         */
        Formset.prototype.hideForm = function($form, remove) {
            var that = this;
            $form.slideUp(300, function() {
                that.afterDeleteForm($form);

                if (remove) {
                    $form.remove()
                }
            });
        };


        /*
            Получение шаблона новой формы
         */
        Formset.prototype.getEmptyForm = function() {
            return this.$root.find('.' + this.opts.emptyFormClass).first();
        };

        /*
            Добавление новой формы.

            Должен вызывать beforeAddForm и afterAddForm.
         */
        Formset.prototype.addForm = function() {
            if (this.beforeAddForm() === false) {
                return
            }

            var $template = this.getEmptyForm();
            if (!$template.length) {
                console.error('Not found empty form template');
                return
            }

            var $form = $template.clone(true).removeClass(this.opts.emptyFormClass);
            $form.hide().appendTo(this.$container);

            // заменяем префикс
            var that = this;
            $form.find('*').each(function() {
                setElementIndex(this, that.nextFormIndex);
            });
            this.nextFormIndex++;

            this.afterAddForm($form);
        };

        Formset.prototype.beforeAddForm = function() {
            // jQuery event
            this.$container.trigger('beforeAddForm.formset');
        };

        Formset.prototype.afterAddForm = function($form) {
            this.showForm($form);

            // jQuery event
            this.$container.trigger('afterAddForm.formset', [$form]);
        };

        /*
            Показ скрытой формы
         */
        Formset.prototype.showForm = function($form) {
            $form.slideDown(300);
        };

        return Formset;
    })();


    /*
     *  Обработчик формсетов с клиентской стороны.
     *
     *  Опции:
     *      prefix:         'form'       - префикс формы
     *      addCssClass:    'add-row'    - CSS-класс кнопки добавления формы
     *      deleteCssClass: 'delete-row' - CSS-класс кнопки удаления формы
     *      emptyCssClass:  'empty-row'  - CSS-класс шаблонной формы
     *      formCssClass:   'form-row'   - CSS-класс нешаблонной кнопки
     *
     *  Опции-события:
     *      maxReached    - Достижение максимального кол-ва форм
     *      minReached    - Достижение минимального кол-ва форм
     *      maxUnreached  - Кол-во форм стало меньше максимума
     *      minUnreached  - Кол-во форм стало больше минимума
     *      addingForm    - Процесс добавления формы
     *      deletingForm  - Процесс удаления формы
     *
     *  При инициализации формсета в HTML уже должны быть установлены
     *  CSS-классы шаблонной и нешаблонных форм. Также должны быть кнопки
     *  удаления форм и кнопка добавления формы с соответствующими CSS-классами.
     *
     *  После инициализации можно управлять формсетом динамически, получив
     *  объект формсета:
     *      var formset = $element.data('formset');
     *
     *      // Добавить новую форму
     *      formset.addForm()
     *
     *      // Удалить первую форму
     *      fs.deleteForm(fs.getForms().first())
     *
     *
     *  Ограничения:
     *      1) кнопка удаления формы должна быть внутри(!) формы
     *      2) шаблонная форма не должна(!) иметь класс options.formCssClass
     *
     **/


    /*
     * Заменяет __prefix__ или индекс элемента el на index
     **/
    /*var updateElementIndex = function(el, prefix, index) {
        var id_regex = new RegExp("(" + prefix + "-(\\d+|__prefix__))"),
            replacement = prefix + "-" + index;

        // label tag
        var for_value = el.getAttribute('for');
        if (for_value) {
            el.setAttribute('for', for_value.replace(id_regex, replacement));
        }

        // ID attr
        if (el.id) {
            el.id = el.id.replace(id_regex, replacement);
        }

        // name attr
        if (el.name) {
            el.name = el.name.replace(id_regex, replacement);
        }
    };*/

    /*window.Formset = function(block, options) {
        var that = this,
            max_reached = false,
            min_reached = false;

        that.root = $(block);
        that.opts = $.extend({}, $.fn.formset.defaults, options);
        that.emptyForm = that.root.find('.' + that.opts.emptyCssClass);
        that.totalForms = $("#id_" + that.opts.prefix + "-TOTAL_FORMS")
            .prop("autocomplete", 'off');
        that.maxForms = $("#id_" + that.opts.prefix + "-MAX_NUM_FORMS")
            .prop("autocomplete", 'off');
        that.minForms = $("#id_" + that.opts.prefix + "-MIN_NUM_FORMS")
            .prop("autocomplete", 'off');

        // Функция установки префикса всем элементам формы
        var setFormIndex = function($form, index) {
            updateElementIndex($form.get(0), that.opts.prefix, index);
            $form.find("*").each(function() {
                updateElementIndex(this, that.opts.prefix, index);
            });
        };

        var isMax = function(forms_count) {
            var maxCount = parseInt(that.maxForms.val()) || 1000;
            return max_reached = forms_count >= maxCount
        };

        var isMin = function(forms_count) {
            var minCount = parseInt(that.minForms.val()) || 0;
            return min_reached = forms_count <= minCount
        };

        // Метод получения всех форм, кроме шаблонной
        that.getForms = function() {
            return that.root.find('.' + that.opts.formCssClass)
        };

        // Метод добавления формы
        that.addForm = function() {
            var row = that.emptyForm.clone(true);
            var forms_count = that.getForms().length;

            if (max_reached) {
                return
            }

            row.removeClass(that.opts.emptyCssClass)
                .addClass(that.opts.formCssClass)
                .attr("id", that.opts.prefix + '-' + forms_count);
            setFormIndex(row, that.totalForms.val());

            // Обновление счетчика форм
            that.totalForms.val(++forms_count);

            // Добавление формы
            that.opts.addingForm.call(that, row);

            // Callback увеличения кол-ва форм после достижения минимума
            if (min_reached && !isMin(forms_count)) {
                that.opts.minUnreached.call(that);
            }

            // Callback достижения максимума форм
            if (isMax(forms_count)) {
                that.opts.maxReached.call(that);
            }

            return false;
        };

        // Метод удаления формы
        that.deleteForm = function(row) {
            if (!row.hasClass(that.opts.formCssClass)) {
                return
            }

            if (min_reached) {
                return
            }

            // Обновление префиксов оставшихся форм
            var forms = that.getForms().filter(function() {
                return this != row.get(0)
            }).each(function(i) {
                setFormIndex($(this), i);
            });

            // Обновление счетчика форм
            that.totalForms.val(forms.length);

            // Удаление формы
            that.opts.deletingForm.call(that, row);

            // Callback уменьшения кол-ва форм после достижения максимума
            if (max_reached && !isMax(forms.length)) {
                that.opts.maxUnreached.call(that);
            }

            // Callback достижения минимума форм
            if (isMin(forms.length)) {
                that.opts.minReached.call(that);
            }

            return false;
        };


        // Устанавливаем ID каждой форме, кроме шаблонной
        var forms = that.getForms().each(function(i) {
            var $form = $(this);
            if (!$form.hasClass(that.opts.emptyCssClass)) {
                $form.prop('id', that.opts.prefix + '-' + i);
            }
        });

        // Проверяем количество форм
        if (isMax(forms.length)) {
            that.opts.maxReached.call(that);
        }
        if (isMin(forms.length)) {
            that.opts.minReached.call(that);
        }

        // Подключаем событие к кнопке добавления
        that.root.find('.' + that.opts.addCssClass)
            .off('.formset')
            .on('click.formset', that.addForm);

        // Подключаем событие к кнопкам удаления
        that.root
            .off('.formset')
            .on('click.formset', '.' + that.opts.deleteCssClass, function() {
                var $form = $(this).closest('.' + that.opts.formCssClass);
                that.deleteForm($form);
            });
    };


    $.fn.formset = function(opts) {
        $(this).data('formset', new Formset(this, opts));
        return this;
    };

    $.fn.formset.defaults = {
        prefix: "form",
        addCssClass: "add-row",
        deleteCssClass: "delete-row",
        emptyCssClass: "empty-row",
        formCssClass: "form-row",

        max_reached: $.noop,
        min_reached: $.noop,
        max_unreached: $.noop,
        min_unreached: $.noop,

        addingForm: function(row) {
            row.insertBefore(this.emptyForm);
        },
        deletingForm: function(row) {
            row.remove();
        }
    };*/

})(jQuery);
