(function($) {
    'use strict';

    var instagram_id = 0;

    window.InstagramWidget = Class(EventedObject, function InstagramWidget(cls, superclass) {
        cls.DATA_KEY = 'instagram';

        cls.defaults = {
            token: '',
            user_id: '',
            limit: 0
        };

        cls.init = function(element, options) {
            superclass.init.call(this);

            this.$root = $(element).first();
            if (!this.$root.length) {
                return this.raise('root element not found');
            }

            // настройки
            var root_data = this.$root.data();
            this.opts = $.extend({}, this.defaults, options);
            this.opts.token = this.opts.token || root_data.access_token;
            if (!this.opts.token) {
                return this.raise('"access_token" undefined');
            }
            this.opts.user_id = this.opts.user_id || root_data.user_id || 'self';
            this.opts.limit = this.opts.limit || parseInt(root_data.limit);

            // отвязывание старого экземпляра
            var old_instance = this.$root.data(this.DATA_KEY);
            if (old_instance) {
                old_instance.destroy();
            }

            // добавление обработчика загрузки
            var that = this;
            this.id = instagram_id++;
            window['instagramWidgetLoaded' + this.id] = function(data) {
                that.onLoad(data);
                delete window['instagramWidgetLoaded' + that.id];
            };

            // запрос данных с Instagram
            this._fetchData();

            this.$root.data(this.DATA_KEY, this);
        };

        cls.destroy = function() {
            this.$root.removeData(this.DATA_KEY);
            superclass.destroy.call(this);
        };

        cls._getFeedURL = function() {
            return 'https://api.instagram.com/v1/users/' + this.opts.user_id +
                   '/media/recent/?access_token=' + this.opts.token +
                   '&count=' + this.opts.limit + '&callback=instagramWidgetLoaded' + this.id;
        };

        cls._fetchData = function() {
            var script = document.createElement('script');
            script.src = this._getFeedURL();
            document.body.appendChild(script);
        };

        /*
            Событие загрузки данных инстаграмма
         */
        cls.onLoad = function(data) {
            if (parseInt(data.meta.code) != 200) {
                this.error(data.meta.error_message + ' (code ' + data.meta.code + ')');
                this.trigger('error', data);
            } else {
                this.trigger('success', data);
            }
        };
    });

    $(document).ready(function() {
        $('.instagram-widget').each(function() {
            window.InstagramWidget(this).on('success', function(response) {
                console.log(response.data)
            });
        })
    });

})(jQuery);