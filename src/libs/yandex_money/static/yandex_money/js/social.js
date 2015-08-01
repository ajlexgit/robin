(function($) {
    
    /*
        Соцкнопки Яндекс.Поделиться.
    */
    
    $.fn.socialButtons = function(options) {
        if (arguments[0] == 'update') {
            // Обновление ссылок
            options = arguments[1];
            return this.each(function() {
                var self = $(this),
                    share = self.data('share');
                
                if (share) {
                    var new_options = {
                        link: options.url || share._default.url,
                        title: options.title || share._default.title,
                        description: options.description || share._default.description,
                        image: options.image || share._default.image
                    };
                    share.updateShareLink(new_options);
                    share._default = new_options;
                } else {
                    console.error('social buttons are not ready yet');
                }
            });
        } else {
            options = arguments[0];
            if (!window.Ya) {
                console.error('window.Ya is not defined');
                return this
            }
            
            return this.each(function() {
                var self = $(this),
                    settings = $.extend(true, {}, $.fn.socialButtons.defaults, self.data(), options);
                
                if (typeof settings.buttons == 'string') {
                    settings.buttons = settings.buttons.split(',');
                }
                
                var share = new Ya.share({
                    element: this.id,
                    elementStyle: {
                        text: '',
                        type: settings.type,
                        border: false,
                        quickServices: settings.buttons
                    },
                    link: settings.url,
                    title: settings.title,
                    description: settings.description,
                    image: settings.image,
                    theme: settings.theme,
                    onready: function(block) {
                        // Функция, вызываемая после инициализации блока
                        self.trigger('ready.yandex-social-buttons', [block]);
                    },
                    onbeforeopen: function(block) {
                        // Функция, вызываемая перед открытием всплывающего окна 
                        self.trigger('beforeopen.yandex-social-buttons', [block]);
                    },
                    onopen: function(block) {
                        // Функция, вызываемая после открытия всплывающего окна
                        self.trigger('open.yandex-social-buttons', [block]);
                    },
                    onbeforeclose: function(block) {
                        // Функция, вызываемая перед закрытием всплывающего окна 
                        self.trigger('beforeclose.yandex-social-buttons', [block]);
                    },
                    onclose: function(block) {
                        // Функция, вызываемая после закрытия всплывающего окна
                        self.trigger('close.yandex-social-buttons', [block]);
                    },
                    onshare: function(service, block) {
                        // Функция, вызываемая после перехода пользователя на сервис
                        self.trigger('share.yandex-social-buttons', [service, block]);
                    }
                });
                
                share._default = {
                    url: settings.url,
                    title: settings.title,
                    description: settings.description,
                    image: settings.image
                };
                
                // Сохранеям объект в элемент
                self.data('share', share);
            })
        }
    };
    
    $.fn.socialButtons.defaults = {
        buttons: 'vkontakte,facebook,twitter,gplus',
        type: 'default',
        theme: 'counter',
        url: '', 
        title: '', 
        description: '', 
        image: ''
    };
    
    
    var init = function() {
        $('.yandex-social-buttons').socialButtons();
    };
    
    // Динамически подключаем скрипт
    var head = document.getElementsByTagName('head')[0];
    var script = document.createElement('script');
    script.onreadystatechange = function () {
        if (this.readyState == 'complete') {
            init();
        }
    };
    script.onload = init;
    script.src = '//yastatic.net/share/share.js';
    head.appendChild(script);
    
})(jQuery);