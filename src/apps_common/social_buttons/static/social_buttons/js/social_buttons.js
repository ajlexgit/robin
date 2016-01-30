(function($) {

    /*
        Базовый класс провайдеров соцкнопок.

        Требует:
            jquery.utils.js

        Получение данных по приоритетам:
            1) data-аттрибут кнопки
            2) data-аттрибут родителя кнопки
            3) Opengraph-тэги
            4) данные на странице (<title>, location.href, ...)

        Возможные аттрибуты:
            data-url
            data-title
            data-image
            data-description

        Пример разметки:
            <div class="social-buttons">
                <div class="social-button social-vk">Share</div>
                <div class="social-button social-fb">Share</div>
                <div class="social-button social-gp">Share</div>
                <div class="social-button social-tw">Share</div>
                <div class="social-button social-li">Share</div>
                <div class="social-button social-pn">Share</div>
            </div>
     */

    var SocialProvider = Class(null, function SocialProvider(cls, superclass) {
        cls.DATA_KEY = 'social';
        cls.WINDOW_WIDTH = 600;
        cls.WINDOW_HEIGHT = 400;

        cls.init = function(button) {
            this.$button = $(button).first();
            if (!this.$button.length) {
                return this.raise('button not found');
            }

            // отвязывание старого экземпляра
            var old_instance = this.$button.data(this.DATA_KEY);
            if (old_instance) {
                old_instance.destroy();
            }

            var that = this;
            this.$button.on(touchClick + '.social', function() {
                var url = that.getShareUrl();
                that.popup(url);
            });

            this.getShareCount();
        };

        cls.destroy = function() {
            this.$button.off('.social');
            this.$button.removeData(this.DATA_KEY);
        };

        cls.updateData = function() {
            var data = this.$button.data();
            var parent_data = this.$button.parent().data();

            // url
            this.url = data.url || parent_data.url;
            if (!this.url) {
                this.url = $('meta[property="og:url"]').attr('content');
            }
            if (!this.url) {
                this.url = location.href;
            }

            // title
            this.title = data.title || parent_data.title;
            if (!this.title) {
                this.title = $('meta[property="og:title"]').attr('content');
            }
            if (!this.title) {
                this.title = $('title').text();
            }

            // image
            this.image = data.image || parent_data.image;
            if (!this.image) {
                this.image = $('meta[property="og:image"]').attr('content');
            }

            // description
            this.description = data.description || parent_data.description;
            if (!this.description) {
                this.description = $('meta[property="og:description"]').attr('content');
            }
            if (!this.description) {
                this.description = $('meta[name="description"]').text();
            }


            if (this.url) {
                this.url = encodeURIComponent(this.url);
            }
            if (this.title) {
                this.title = encodeURIComponent(this.title);
            }
            if (this.image) {
                this.image = encodeURIComponent(this.image);
            }
            if (this.description) {
                this.description = encodeURIComponent(this.description);
            }
        };

        cls.getShareUrl = function() {
            this.updateData();
            return '';
        };

        cls.getShareCount = function() {
            this.updateData();
            return '';
        };

        cls._shareCountScript = function(url) {
            var script = document.createElement('script'),
                head = document.head;

            script.type = 'text/javascript';
            script.src = url;

            head.appendChild(script);
            head.removeChild(script);
        };

        cls.shareCountFetched = function(count) {
            if (typeof count != 'undefined') {
                var $counter = this.$button.find('.counter');
                if ($counter.length) {
                    $counter.text(count)
                } else {
                    this.$button.append(
                        $('<span/>').addClass('counter').text(count)
                    );
                }
            }
        };

        cls.popup = function(url, winId, width, height) {
            var browser_left = typeof window.screenX != 'undefined' ? window.screenX : window.screenLeft,
                browser_top = typeof window.screenY != 'undefined' ? window.screenY : window.screenTop,
                browser_width = typeof window.outerWidth != 'undefined' ? window.outerWidth : document.body.clientWidth,
                browser_height = typeof window.outerHeight != 'undefined' ? window.outerHeight : document.body.clientHeight,
                popup_width = width || this.WINDOW_WIDTH,
                popup_height = height || this.WINDOW_HEIGHT,
                top_position = browser_top + Math.round((browser_height - popup_height) / 2),
                left_position = browser_left + Math.round((browser_width - popup_width) / 2);

            var win = window.open(
                url,
                winId || this.__name__,
                'width=' + popup_width + ', ' +
                'height=' + popup_height + ', ' +
                'top=' + top_position + ', ' +
                'left=' + left_position
            );

            if (!win) {
                return location.href = url;
            }

            win.focus();

            return win;
        }
    });

    /*
        Провайдер ВКонтакте
     */
    var VkProvider = Class(SocialProvider, function VkProvider(cls, superclass) {
        cls.getShareUrl = function() {
            superclass.getShareUrl.call(this);

            var params = '?';
            if (this.url) {
                params += 'url=' + this.url + '&';
            }
            if (this.title) {
                params += 'title=' + this.title + '&';
            }
            if (this.image) {
                params += 'image=' + this.image + '&';
            }
            if (this.description) {
                params += 'description=' + this.description + '&';
            }

            return 'http://vk.com/share.php' + params;
        };

        cls.getShareCount = function() {
            superclass.getShareCount.call(this);

            var obj = window;
            var keys = ['VK', 'Share'];
            $.each(keys, function(i, key) {
                if (typeof obj[key] === 'undefined') {
                    obj[key] = {};
                }

                obj = obj[key];
            });

            var that = this;
            window.VK.Share.count = function(index, count) {
                that.shareCountFetched(count);
            };

            this._shareCountScript('http://vk.com/share.php?act=count&url=' + this.url);
        };
    });

    /*
        Провайдер Facebook
     */
    var FacebookProvider = Class(SocialProvider, function FacebookProvider(cls, superclass) {
        cls.getShareUrl = function() {
            superclass.getShareUrl.call(this);

            var params = '?';
            if (this.url) {
                params += 'u=' + this.url + '&';
            }

            return 'http://www.facebook.com/sharer/sharer.php' + params;
        };

        cls.getShareCount = function() {
            superclass.getShareCount.call(this);

            var that = this;
            window.social_facebook = function(data) {
                that.shareCountFetched(data[0]['total_count']);
            };

            this._shareCountScript('https://api.facebook.com/method/links.getStats?urls=' + this.url + '&format=json&callback=social_facebook');
        };
    });

    /*
        Провайдер Twitter
     */
    var TwitterProvider = Class(SocialProvider, function TwitterProvider(cls, superclass) {
        cls.WINDOW_WIDTH = 600;
        cls.WINDOW_HEIGHT = 300;

        cls.getShareUrl = function() {
            superclass.getShareUrl.call(this);

            var params = '?';
            if (this.url) {
                params += 'url=' + this.url + '&';
            }
            if (this.description) {
                params += 'text=' + this.description + '&';
            }

            return 'http://twitter.com/share' + params;
        };
    });

    /*
        Провайдер GooglePlus
     */
    var GooglePlusProvider = Class(SocialProvider, function GooglePlusProvider(cls, superclass) {
        cls.WINDOW_WIDTH = 600;
        cls.WINDOW_HEIGHT = 500;

        cls.getShareUrl = function() {
            superclass.getShareUrl.call(this);

            var params = '?';
            if (this.url) {
                params += 'url=' + this.url + '&';
            }

            return 'https://plus.google.com/share' + params;
        };

        cls.getShareCount = function() {
            superclass.getShareCount.call(this);

            var obj = window;
            var keys = ['services', 'gplus'];
            $.each(keys, function(i, key) {
                if (typeof obj[key] === 'undefined') {
                    obj[key] = {};
                }

                obj = obj[key];
            });

            var that = this;
            window.services.gplus.cb = function(count) {
                that.shareCountFetched(parseInt(count));
            };

            this._shareCountScript('http://share.yandex.ru/gpp.xml?url=' + this.url);
        };
    });

    /*
        Провайдер LinkedIn
    */
    var LinkedInProvider = Class(SocialProvider, function LinkedInProvider(cls, superclass) {
        cls.WINDOW_WIDTH = 600;
        cls.WINDOW_HEIGHT = 500;

        cls.getShareUrl = function() {
            superclass.getShareUrl.call(this);

            var params = '?mini=true&';
            if (this.url) {
                params += 'url=' + this.url + '&';
            }
            if (this.title) {
                params += 'title=' + this.title + '&';
            }
            if (this.image) {
                params += 'image=' + this.image + '&';
            }
            if (this.description) {
                params += 'summary=' + this.description + '&';
            }

            return 'http://www.linkedin.com/shareArticle' + params;
        };

        cls.getShareCount = function() {
            superclass.getShareCount.call(this);

            var that = this;
            window.social_linkedIn = function(data) {
                that.shareCountFetched(data['count']);
            };

            this._shareCountScript('https://www.linkedin.com/countserv/count/share?url=' + this.url + '&callback=social_linkedIn');
        };
    });

    /*
        Провайдер Pinterest
    */
    var PinterestProvider = Class(SocialProvider, function PinterestProvider(cls, superclass) {
        cls.WINDOW_WIDTH = 760;
        cls.WINDOW_HEIGHT = 600;

        cls.getShareUrl = function() {
            superclass.getShareUrl.call(this);

            var params = '?';
            if (this.url) {
                params += 'url=' + this.url + '&';
            }
            if (this.image) {
                params += 'media=' + this.image + '&';
            }
            if (this.description) {
                params += 'description=' + this.description + '&';
            }

            return 'http://www.pinterest.com/pin/create/button/' + params;
        };

        cls.getShareCount = function() {
            superclass.getShareCount.call(this);

            var that = this;
            window.social_pinterest = function(data) {
                that.shareCountFetched(data['count']);
            };

            this._shareCountScript('http://widgets.pinterest.com/v1/urls/count.json?url=' + this.url + '&callback=social_pinterest');
        };
    });

    $(document).ready(function() {
        VkProvider('.social-vk');
        FacebookProvider('.social-fb');
        TwitterProvider('.social-tw');
        GooglePlusProvider('.social-gp');
        LinkedInProvider('.social-li');
        PinterestProvider('.social-pn');
    });

})(jQuery);