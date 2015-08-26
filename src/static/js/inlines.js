(function($) {

    /*
        Модуль для работы с inline-формами на клиенте.

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
            this.$root = $.findFirstElement(root);
            if (!this.$root.length) {
                console.error('Empty root element for Formset');
                return
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
            var initial_count = parseInt(this.management.$initial_forms.val()) || 0;
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
                formClass: 'form',
                emptyFormClass: 'empty-form',

                prefix: 'form',

                beforeAddForm: $.noop,
                afterAddForm: $.noop,
                beforeDeleteForm: $.noop,
                afterDeleteForm: $.noop
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
            Получение шаблона новой формы
         */
        Formset.prototype.getEmptyForm = function() {
            return this.$root.find('.' + this.opts.emptyFormClass).first();
        };

        /*
            Установка или получение значения DELETE-поля формы
         */
        Formset.prototype.formDeleted = function(form_selector, value) {
            var $form = $.findFirstElement(form_selector, this.$container);
            if (!$form.length) {
                console.error('Not found form');
                return
            }

            var $field = $form.find('[name^="' + this.opts.prefix + '-"][name$="-DELETE"]').first();
            var field_type = $field.prop('type');
            if (value == undefined) {
                // получение значения
                if ((field_type == 'checkbox') || (field_type == 'radio')) {
                    return $field.prop('checked');
                } else {
                    return Boolean($field.val()) || false;
                }
            } else {
                // установка значения
                value = Boolean(value) || false;
                if ((field_type == 'checkbox') || (field_type == 'radio')) {
                    return $field.prop('checked', value);
                } else {
                    return $field.val(Number(value))
                }
            }
        };


        /*
            Удаление формы. Устанавливает поле DELETE, если оно есть.
            Если установлен hide_form, будет вызвана анимация скрытия формы.

            Должен вызывать beforeDeleteForm и afterDeleteForm.

            Возвращает jQuery-объект удаленной формы или false
         */
        Formset.prototype.deleteForm = function(form_selector, hide_form) {
            var $form = $.findFirstElement(form_selector, this.$container);
            if (!$form.length) {
                console.error('Not found form to be deleted');
                return false
            }

            if (this.beforeDeleteForm($form) === false) {
                return false
            }

            this.formDeleted($form, true);

            if (hide_form) {
                this.hideForm($form);
            } else {
                this.afterDeleteForm($form);
            }

            return $form;
        };

        Formset.prototype.beforeDeleteForm = function($form) {
            // ищем кол-во форм, которые не помечены удаленными
            var that = this;
            var final_count = 0;
            var $forms = this.getForms();
            $forms.each(function() {
                if (!that.formDeleted(this)) {
                    final_count++;
                }
            });

            // предотвращаем добавление, если превышено кол-во форм
            var min_num_forms = parseInt(this.management.$min_num_forms.val()) || 0;
            if (final_count <= min_num_forms) {
                return false;
            }

            // jQuery event
            this.$container.trigger('beforeDeleteForm.formset', [$form]);

            return this.opts.beforeDeleteForm.call(this, $form);
        };

        Formset.prototype.afterDeleteForm = function($form) {
            this.opts.afterDeleteForm.call(this, $form);

            // jQuery event
            this.$container.trigger('afterDeleteForm.formset', [$form]);
        };

        /*
            Скрытие (с возможным удалением) формы.

            Должен вызывать afterDeleteForm.
         */
        Formset.prototype.hideForm = function($form) {
            var that = this;
            $form.slideUp(300, function() {
                var form_data = $form.data();
                if (!form_data.initial) {
                    $form.remove();

                    // уменьшаем TOTAL_FORMS
                    var total_forms = parseInt(that.management.$total_forms.val()) || 0;
                    that.management.$total_forms.val(--total_forms);
                }

                that.afterDeleteForm($form);
            });
        };


        /*
            Добавление новой формы.

            Должен вызывать beforeAddForm и afterAddForm.

            Возвращает jQuery-объект новой формы или false
         */
        Formset.prototype.addForm = function() {
            if (this.beforeAddForm() === false) {
                return false
            }

            var $template = this.getEmptyForm();
            if (!$template.length) {
                console.error('Not found empty form template');
                return false
            }

            var $form = $template.clone(true).removeClass(this.opts.emptyFormClass);
            $form.hide().appendTo(this.$container);

            // увеличиваем TOTAL_FORMS
            var total_forms = parseInt(this.management.$total_forms.val()) || 0;
            this.management.$total_forms.val(++total_forms);

            // заменяем префикс
            var that = this;
            $form.find('*').each(function() {
                setElementIndex(this, that.nextFormIndex);
            });
            this.nextFormIndex++;

            this.afterAddForm($form);

            return $form;
        };

        Formset.prototype.beforeAddForm = function() {
            // ищем кол-во форм, которые не помечены удаленными
            var that = this;
            var final_count = 0;
            var $forms = this.getForms();
            $forms.each(function() {
                if (!that.formDeleted(this)) {
                    final_count++;
                }
            });

            // предотвращаем добавление, если превышено кол-во форм
            var max_num_forms = parseInt(this.management.$max_num_forms.val()) || 1000;
            if (final_count >= max_num_forms) {
                return false;
            }

            // jQuery event
            this.$container.trigger('beforeAddForm.formset');

            return this.opts.beforeAddForm.call(this);
        };

        Formset.prototype.afterAddForm = function($form) {
            this.opts.afterAddForm.call(this, $form);

            // jQuery event
            this.$container.trigger('afterAddForm.formset', [$form]);

            this.showForm($form);
        };

        /*
            Показ скрытой формы
         */
        Formset.prototype.showForm = function($form) {
            $form.slideDown(300);
        };

        return Formset;
    })();

})(jQuery);
