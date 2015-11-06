(function($) {

    /*
        Модуль для работы с inline-формами на клиенте.

        Требует:
            jquery.utils.js

        Параметры:
            formsContainerSelector      - селектор контейнера форм
            formClass                   - класс каждой формы
            emptyFormClass              - класс пустой формы, которая является шаблоном для добавления
            prefix                      - Django-префикс формы
            showSpeed                   - скорость показа новой формы при добавлении
            hideSpeed                   - скорость скрытия формы при удалении
            beforeAddForm               - событие, вызываемое перед добавлением новой формы.
                                          Если вернёт false, форма не будет добавлена
            afterAddForm                - событие, вызываемое после добавления новой формы
            beforeDeleteForm            - событие, вызываемое перед удалением формы.
                                          Если вернёт false, форма не будет удалена
            afterDeleteForm             - событие, вызываемое после удаления формы

        Пример:
            HTML:
              <div id="formset">
                  {{ formset.management_form }}

                  <div class="forms">
                    {% for form in formset %}
                      <div class="form">
                        {{ form }}
                      </div>
                    {% endfor %}
                  </div>

                  <script type="text/template" class="form-template">
                     {% with form=formset.empty_form %}
                      <div class="form">
                         {{ form }}
                      </div>
                    {% endwith %}
                  </script>
              </div>

            JS:
              fs = Formset.create('#formset');
              fs.addForm();
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

    window.Formset = Class(null, function(cls, superclass) {
        var dataParamName = 'formset';

        cls.init = function(root, options) {
            this.$root = $(root).first();
            if (!this.$root.length) {
                console.error('Formset can\'t find root element');
                return false;
            } else {
                // отвязывание старого экземпляра
                var old_instance = this.$root.data(dataParamName);
                if (old_instance) {
                    old_instance.destroy();
                }
                this.$root.data(dataParamName, this);
            }

            this.opts = $.extend({
                formsContainerSelector: '.forms',
                formClass: 'form',
                emptyFormClass: 'empty-form',

                prefix: 'form',
                showSpeed: 300,
                hideSpeed: 300,

                beforeAddForm: function() {
                    return this.getFormCount() < this.getMaxFormCount();
                },
                afterAddForm: $.noop,

                // перед удалением формы
                beforeDeleteForm: function() {
                    return this.getFormCount() > this.getMinFormCount()
                },
                afterDeleteForm: $.noop
            }, options);

            // management form
            this.management = this.getManagementForm();
            if (this.management === false) {
                return false;
            }

            // контейнер форм
            this.$container = this.$root.find(this.opts.formsContainerSelector);
            if (!this.$container.length) {
                console.error('Formset can\'t find forms container element');
                return false;
            }

            // Находим начальные формы
            var $initial_forms = this.getForms();

            // индекс следующей добавляемой формы
            this.nextFormIndex = $initial_forms.length;

            // Помечаем начальные формы
            var initial_count = parseInt(this.management.$initial_forms.val()) || 0;
            if ($initial_forms.length < initial_count) {
                console.error('INITIAL_FORMS is less than real forms count');
                return false
            }
            $initial_forms.slice(0, initial_count).data('initial', true);
        };

        /*
            Отвязывание плагина
         */
        cls.prototype.destroy = function() {
            this.$root.removeData(dataParamName);
        };

        /*
            Получение полей management-формы
         */
        cls.prototype.getManagementForm = function() {
            var $total_forms = $('#id_' + this.opts.prefix + '-TOTAL_FORMS');
            var $initial_forms = $('#id_' + this.opts.prefix + '-INITIAL_FORMS');
            var $min_num_forms = $('#id_' + this.opts.prefix + '-MIN_NUM_FORMS');
            var $max_num_forms = $('#id_' + this.opts.prefix + '-MAX_NUM_FORMS');

            if (!$total_forms.length) {
                console.error('Not found TOTAL_FORMS field');
                return false
            }
            if (!$initial_forms.length) {
                console.error('Not found INITIAL_FORMS field');
                return false
            }
            if (!$min_num_forms.length) {
                console.error('Not found MIN_NUM_FORMS field');
                return false
            }
            if (!$max_num_forms.length) {
                console.error('Not found MAX_NUM_FORMS field');
                return false
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
        cls.prototype.getForms = function(with_deleted) {
            var that = this;
            var $forms = this.$container.find('.' + this.opts.formClass);
            if (!with_deleted) {
                $forms = $forms.filter(function(i, item) {
                    return !that.formDeleted(item);
                })
            }
            return $forms;
        };

        /*
            Получение количества всех форм
         */
        cls.prototype.getFormCount = function(with_deleted) {
            return this.getForms(with_deleted).length;
        };

        /*
            Получение минимального количества всех форм
         */
        cls.prototype.getMinFormCount = function() {
            return parseInt(this.management.$min_num_forms.val()) || 0;
        };

        /*
            Получение максимального количества всех форм
         */
        cls.prototype.getMaxFormCount = function() {
            return parseInt(this.management.$max_num_forms.val()) || 1000;
        };

        /*
            Получение шаблона новой формы
         */
        cls.prototype.getEmptyForm = function() {
            var $template = this.$root.find('.' + this.opts.emptyFormClass).first();
            if (!$template.length) {
                console.error('Not found empty form template');
                return $()
            }

            return $($template.html());
        };

        // =====================================================

        /*
            Установка или получение значения DELETE-поля формы
         */
        cls.prototype.formDeleted = function(form_selector, value) {
            var $form = this.$container.find(form_selector).first();
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
            Добавление новой формы.

            Возвращает jQuery-объект новой формы или false
         */
        cls.prototype.addForm = function() {
            if (this.opts.beforeAddForm.call(this) === false) {
                return false
            }

            var $form = this.getEmptyForm();
            $form.hide().appendTo(this.$container);

            // увеличиваем TOTAL_FORMS
            var total_forms = this.getFormCount(true);
            this.management.$total_forms.val(total_forms);

            // заменяем префикс
            var that = this;
            $form.find('*').each(function() {
                setElementIndex(this, that.nextFormIndex);
            });
            this.nextFormIndex++;

            // анимация показа
            $form.slideDown({
                duration: this.opts.showSpeed,
                complete: function() {
                    that.opts.afterAddForm.call(this, $form);
                }
            });

            return $form;
        };


        /*
            Удаление формы. Устанавливает поле DELETE, если оно есть.

            Возвращает jQuery-объект удаленной формы или false
         */
        cls.prototype.deleteForm = function(form_selector) {
            if (this.opts.beforeDeleteForm.call(this) === false) {
                return false
            }

            var $form = this.$container.find(form_selector);
            if (!$form.length) {
                console.error('Not found form to be deleted');
                return false
            }

            this.formDeleted($form, true);

            var that = this;

            // анимация удаления
            $form.slideUp({
                duration: that.opts.hideSpeed,
                complete: function() {
                    var form_data = $form.data();
                    if (!form_data.initial) {
                        $form.remove();

                        // уменьшаем TOTAL_FORMS
                        var total_forms = that.getFormCount(true);
                        that.management.$total_forms.val(total_forms);
                    }

                    that.opts.afterDeleteForm.call(this, $form);
                }
            });

            return $form;
        };
    });

})(jQuery);
