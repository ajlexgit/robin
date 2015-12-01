(function($) {

    /*
        Модуль для работы с inline-формами на клиенте.

        Требует:
            jquery.utils.js

        Параметры:
            prefix              - Django-префикс форм
            formsListSelector   - селектор контейнера, в который будут добавляться новые формы.
            formSelector        - селектор каждого блока формы в контейнере
            formTemplate        - селектор контейнера пустой формы

            showSpeed           - скорость показа новой формы при добавлении
            hideSpeed           - скорость скрытия формы при удалении

            beforeAddForm       - событие, вызываемое перед добавлением новой формы.
                                  Если вернёт false, форма не будет добавлена
            afterAddForm        - событие, вызываемое после добавления новой формы
            beforeDeleteForm    - событие, вызываемое перед удалением формы.
                                  Если вернёт false, форма не будет удалена
            afterDeleteForm     - событие, вызываемое после удаления формы

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
                     <div class="form">
                        {{ formset.empty_form }}
                     </div>
                  </script>
              </div>

            JS:
              fs = Formset.create('#formset', {
                  prefix: 'inlines'
              });

              // добавление формы
              var $form = fs.addForm();

              // удаление формы
              fs.deleteForm($form);
     */

    /*
        Замена "__prefix__" в форме на реальный индекс формы
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

    window.ManagementForm = Class(null, function(cls, superclass) {
        cls.init = function(root, prefix) {
            this.$root = $(root).first();
            if (!this.$root.length) {
                console.error('ManagementForm: root element not found');
                return false;
            }

            if (!prefix) {
                console.error('ManagementForm: prefix required');
                return false;
            }

            this.$total_forms = this.$root.find('#id_' + prefix + '-TOTAL_FORMS');
            this.$initial_forms = this.$root.find('#id_' + prefix + '-INITIAL_FORMS');
            this.$min_num_forms = this.$root.find('#id_' + prefix + '-MIN_NUM_FORMS');
            this.$max_num_forms = this.$root.find('#id_' + prefix + '-MAX_NUM_FORMS');

            if (!this.$total_forms.length) {
                console.error('ManagementForm: not found TOTAL_FORMS field');
                return false
            }
            if (!this.$initial_forms.length) {
                console.error('ManagementForm: not found INITIAL_FORMS field');
                return false
            }
            if (!this.$min_num_forms.length) {
                console.error('ManagementForm: not found MIN_NUM_FORMS field');
                return false
            }
            if (!this.$max_num_forms.length) {
                console.error('ManagementForm: not found MAX_NUM_FORMS field');
                return false
            }
        };

        cls.prototype.getTotalFormCount = function() {
            return parseInt(this.$total_forms.val()) || 0;
        };

        cls.prototype.getInitialFormCount = function() {
            return parseInt(this.$initial_forms.val()) || 0;
        };

        cls.prototype.getMinFormCount = function() {
            return parseInt(this.$min_num_forms.val()) || 0;
        };

        cls.prototype.getMaxFormCount = function() {
            return parseInt(this.$max_num_forms.val()) || 1000;
        };
    });

    window.Formset = Class(null, function(cls, superclass) {
        cls.init = function(root, options) {
            this.$root = $(root).first();
            if (!this.$root.length) {
                console.error('Formset: root element not found');
                return false;
            }

            this.opts = $.extend({
                prefix: '',
                formsListSelector: '.forms',
                formSelector: '.form',
                formTemplate: '.empty-form',
                showSpeed: 300,
                hideSpeed: 300,
                beforeAddForm: function() {
                    return this.getFormCount() < this.management.getMaxFormCount();
                },
                afterAddForm: $.noop,
                beforeDeleteForm: function() {
                    return this.getFormCount() > this.management.getMinFormCount()
                },
                afterDeleteForm: $.noop
            }, options);

            if (!this.opts.prefix) {
                console.error('Formset: prefix required');
                return false;
            }

            // management form
            this.management = ManagementForm.create(this.$root, this.opts.prefix);
            if (!this.management) {
                return false;
            }

            // контейнер форм
            this.$formContainer = this.$root.find(this.opts.formsListSelector);
            if (!this.$formContainer.length) {
                console.error('Formset: forms container not found');
                return false;
            }

            // шаблон форм
            this.$template = this.$root.find(this.opts.formTemplate);
            if (!this.$template.length) {
                console.error('Formset: form template not found');
                return false;
            }

            // все формы
            var $forms = this.getForms();
            if ($forms.length != this.management.getTotalFormCount()) {
                console.error('Formset: management TOTAL_FORMS is less than real form count');
                return false;
            }

            // начальные формы
            this.$initial_forms = $forms.slice(0, this.management.getInitialFormCount());
            if (this.$initial_forms.length != this.management.getInitialFormCount()) {
                console.error('Formset: management INITIAL_FORMS is less than real form count');
                return false;
            }

            // отвязывание старого экземпляра
            var old_instance = this.$root.data(cls.dataParamName);
            if (old_instance) {
                old_instance.destroy();
            }

            // индекс следующей добавляемой формы
            this._nextFormIndex = this.$initial_forms.length;

            this.$root.data(cls.dataParamName, this);
        };

        /*
            Отвязывание плагина
         */
        cls.prototype.destroy = function() {
            this.$root.removeData(cls.dataParamName);
        };

        /*
            Получение всех форм
         */
        cls.prototype.getForms = function() {
            return this.$formContainer.find(this.opts.formSelector);
        };

        /*
            Получение поля удаления формы
         */
        cls.prototype.getDeleteField = function(form) {
            var $form = $(form).first();
            if (!$form.length) {
                console.error('Formset: not found form to find delete field');
                return false;
            }

            var $field = $form.find('[name^="' + this.opts.prefix + '-"][name$="-DELETE"]');
            return $field.first();
        };

        /*
            Является ли форма начальной
         */
        cls.prototype.isInitial = function(form) {
            var $form = $(form).first();
            if (!$form.length) {
                console.error('Formset: not found form to check initial');
                return false;
            }

            return this.$initial_forms.toArray().indexOf($form.get(0)) >= 0;
        };

        /*
            Получение кол-ва активных форм
         */
        cls.prototype.getFormCount = function() {
            var that = this;
            var $forms = this.getForms();
            return $forms.filter(function(i, form) {
                var $df = that.getDeleteField($(form));
                if ($df.length) {
                    return !$df.prop('checked');
                } else {
                    console.warn('Formset: delete field not found');
                    return true
                }
            }).length
        };

        /*
            Получение новой формы
         */
        cls.prototype.getEmptyForm = function() {
            var that = this;
            var $form = $(this.$template.html());
            $form.find('*').each(function() {
                setElementIndex(this, that._nextFormIndex);
            });
            that._nextFormIndex++;
            return $form;
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
            $form.hide().appendTo(this.$formContainer);

            // увеличиваем TOTAL_FORMS
            var total_forms = this.management.getTotalFormCount();
            this.management.$total_forms.val(total_forms + 1);

            // анимация показа
            var that = this;
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
        cls.prototype.deleteForm = function(form) {
            var $form = $(form).first();
            if (!$form.length) {
                console.error('Formset: not found form to delete');
                return false
            }

            if (this.opts.beforeDeleteForm.call(this, $form) === false) {
                return false
            }

            var $df = this.getDeleteField($form);
            if ($df.length) {
                // форма уже удалена
                if ($df.prop('checked')) {
                    return $form;
                }

                $df.prop('checked', true);
            } else {
                console.warn('Formset: delete field not found');
            }

            // анимация удаления
            var that = this;
            $form.slideUp({
                duration: that.opts.hideSpeed,
                complete: function() {
                    if (!that.isInitial($form)) {
                        $form.remove();

                        // уменьшаем TOTAL_FORMS
                        var total_forms = that.management.getTotalFormCount();
                        that.management.$total_forms.val(total_forms - 1);
                    }

                    that.opts.afterDeleteForm.call(this, $form);
                }
            });

            return $form;
        };
    });
    Formset.dataParamName = 'formset';

})(jQuery);