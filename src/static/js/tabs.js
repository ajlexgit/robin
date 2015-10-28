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

    window.TabManager = (function() {
        var TabManager = function() {};

        TabManager.create = function(root, options) {
            var self = new TabManager();

            self.$root = $.findFirstElement(root);
            if (!self.$root.length) {
                console.warn('TabManager can\'t find root element');
                return
            }

            // opts
            self.opts = $.extend(self.getDefaultOpts(), options);

            // определяем текущую вкладку
            var $current = $.findFirstElement(self.opts.tabSelector + '.' + self.opts.tabVisibleClass, self.$root);
            self.setCurrentTab($current);

            // events
            self.$root.off('click.tabmanger');
            self.$root.on('click.tabmanger', '[data-tab]', function() {
                var tabName = $(this).data('tab');
                self.openTab(tabName);
                return false;
            });

            self.$root.on('click.tabmanger', '[data-tab-back]', function() {
                var tabName = self.opts.getBackTabName.call(self, self.currentTabName);
                self.openTab(tabName);
                return false;
            });

            self.$root.data('tabmanager', self);

            return self;
        };

        TabManager.prototype.getDefaultOpts = function() {
            return {
                tabSelector: '.tab',
                tabVisibleClass: 'visible',

                getBackTabName: function(tabName) {
                    // имя предыдущей вкладки
                    return tabName.split('-').slice(0, -1).join('-');
                },

                beforeCloseTab: function($tab, tabName) {
                    // перед закрытием текущей вкладки
                },
                closeTab: function($tab, tabName) {
                    // закрытие вкладки
                    $tab.removeClass(this.opts.tabVisibleClass);
                },

                beforeShowTab: function($tab, tabName) {
                    // перед показом вкладки
                },
                showTab: function($tab, tabName) {
                    // показ вкладки
                    $tab.addClass(this.opts.tabVisibleClass);
                }
            }
        };


        /*
            Установка текущей вкладки и её имени
         */
        TabManager.prototype.setCurrentTab = function($tab, tabName) {
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
        TabManager.prototype.getTabByName = function(tabName) {
            return $.findFirstElement(this.opts.tabSelector + '.' + tabName, this.$root);
        };


        /*
            Показ вкладки
         */
        TabManager.prototype.openTab = function(tabName) {
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

        return TabManager;
    })();

})(jQuery);