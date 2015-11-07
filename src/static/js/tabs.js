(function($) {

    /*
        Менеджер, отвечающий за переключение вкладок.

        Требует:
            jquery.utils.js

        Каждая вкладка имеет имя, которое по умолчанию указывается
        в CSS-классах в виде "tab-NAME".

        Ссылка для открытия вкладки может быть любым DOM-элементом
        с аттрибутом "data-tab", в котором хранится имя вкладки:
            <a data-tab="tab-one">...</a>

        Особый случай - ссылка для возврата на предыдущую вкладку.
        Иерархия вкладок может быть осуществлена через имя вкладки:
            tab-one
                tab-one-one
                tab-one-two

            tab-two
                tab-two-one

        Для ссылки возврата должен быть установлен аттрибут "data-tab-back":
            <a data-tab-back>...</a>


        Параметры:
            tabSelector         - селектор вкладок внутри $root
            tabVisibleClass     - класс видимой вкладки
            getBackTabName      - определение предыдущей вкладки для возврата
            beforeCloseTab      - событие перед закрытием вкладки
            closeTab            - событие закрытия вкладки
            beforeShowTab       - событие перед показом вкладки
            showTab             - событие показа вкладки

        Пример:
            HTML:
              <div id="tabs">
                <div class="tab tab-one visible">
                  <p>Tab №1.1</p>
                  <p><a href="#" data-tab="tab-two">tab 2</a></p>
                </div>

                <div class="tab tab-two">
                  <p>Tab №2.1</p>
                  <p><a href="#" data-tab-back>back</a></p>
                </div>

                <div class="tab tab-two-two">
                  <p>Tab №2.2</p>
                  <p><a href="#" data-tab-back>back</a></p>
                </div>
              </div>

            JS:
              var tm = TabManager.create('#tabs');

              // открыть вторую вкладку
              tm.openTab('tab-two')
     */

    window.TabManager = Class(null, function(cls, superclass) {
        cls.init = function(root, options) {
            this.$root = $(root).first();
            if (!this.$root.length) {
                console.error('TabManager can\'t find root element');
                return false;
            } else {
                // отвязывание старого экземпляра
                var old_instance = this.$root.data(TabManager.dataParamName);
                if (old_instance) {
                    old_instance.destroy();
                }
                this.$root.data(TabManager.dataParamName, this);
            }

            // настройки
            this.opts = $.extend({
                tabSelector: '.tab',
                tabVisibleClass: 'visible',

                getBackTabName: function(tabName) {
                    return tabName.split('-').slice(0, -1).join('-');
                },
                beforeCloseTab: function($tab, tabName) {

                },
                closeTab: function($tab, tabName) {
                    $tab.removeClass(this.opts.tabVisibleClass);
                },
                beforeShowTab: function($tab, tabName) {

                },
                showTab: function($tab, tabName) {
                    $tab.addClass(this.opts.tabVisibleClass);
                }
            }, options);

            // определяем текущую вкладку
            var $current = this.$root.find(this.opts.tabSelector + '.' + this.opts.tabVisibleClass);
            this.setCurrentTab($current);

            var that = this;

            // клик на ссылке открытия вкладки
            this.$root.on('click.tabmanger', '[data-tab]', function() {
                var tabName = $(this).data('tab');
                that.openTab(tabName);
                return false;
            });

            // клик на ссылке открытия предыдущей вкладки
            this.$root.on('click.tabmanger', '[data-tab-back]', function() {
                var tabName = that.opts.getBackTabName.call(that, that.currentTabName);
                that.openTab(tabName);
                return false;
            });
        };

        /*
            Отвязывание плагина
         */
        cls.prototype.destroy = function() {
            this.$root.off('.tabmanger');
            this.$root.removeData(TabManager.dataParamName);
        };


        /*
            Установка текущей вкладки и её имени
         */
        cls.prototype.setCurrentTab = function($tab, tabName) {
            this.$currentTab = $tab;
            if (tabName) {
                this.currentTabName = tabName;
            } else {
                var match = /\btab-([^\s]+)\b/.exec($tab.prop('className'));
                if (match && match[1]) {
                    this.currentTabName = match[0]
                } else {
                    this.currentTabName = ''
                }
            }
        };

        /*
            Получение вкладки по её имени
         */
        cls.prototype.getTabByName = function(tabName) {
            return this.$root.find(this.opts.tabSelector + '.' + tabName);
        };

        /*
            Показ вкладки
         */
        cls.prototype.openTab = function(tabName) {
            if (!tabName) {
                return
            }

            var $tab = this.getTabByName(tabName);
            if (!$tab || !$tab.length) {
                console.warn('TabManager can\'t find tab "' + tabName + '"');
                return
            }

            // закрытие текущей вкладки
            if (this.$currentTab && this.$currentTab.length) {
                this.opts.beforeCloseTab.call(this, this.$currentTab, this.currentTabName);
                this.opts.closeTab.call(this, this.$currentTab, this.currentTabName);
            }

            // открытие новой вкладки
            this.opts.beforeShowTab.call(this, $tab, tabName);
            this.opts.showTab.call(this, $tab, tabName);

            this.$currentTab = $tab;
            this.currentTabName = tabName;
        };
    });
    TabManager.dataParamName = 'tabs';


    $.fn.tabManager = function(options) {
        return this.each(function() {
            TabManager.create(this, options);
        })
    }

})(jQuery);