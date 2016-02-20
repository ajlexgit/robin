(function($) {
    'use strict';

    /*
        https://developer.vimeo.com/player/js-api

        Требует:
            jquery.utils.js

        Параметры:
            video       - строка с ключем видео
            autoplay    - автоматически начать показ

        События:
            // Видео готово к воспроизведению
            ready

            // Видео начало воспроизводиться
            play

            // Видео перестало воспроизводиться
            pause

            // Видео закончилось
            ended

        Пример:
            <div id="player"></div>

            <script>
                var player = Vimeo('#player', {
                    video: '116908919'
                }).on('ready', function() {
                    this.position(60);
                });

                // запуск видео
                player.play();

                // пауза
                player.pause();

                // остановка видео
                player.stop();

                // перемотка на позицию в секундах от начала
                player.position(60);

                // громкость на 50%
                player.position(50);
            </script>
    */

    window.Vimeo = Class(EventedObject, function Vimeo(cls, superclass) {
        cls.defaults = {
            video: '',
            autoplay: false
        };

        cls.init = function(container, options) {
            superclass.init.call(this);

            this.$container = $(container).first();
            if (!this.$container.length) {
                return this.raise('container element not found');
            }

            this.opts = $.extend({}, this.defaults, options);

            if (!this.opts.video) {
                return this.raise('video ID required');
            }

            var that = this;
            window.Vimeo.ready(function() {
                that.makeNative();
            });
        };

        /*
            Освобождение ресурсов
         */
        cls.destroy = function() {
            this.stop();
            if (this.native) {
                this.$iframe.replaceWith(this._containerHTML);
                this.$iframe = null;
                this.native = null;
            }
            superclass.destroy.call(this);
        };

        /*
            Создание нативного объекта
         */
        cls.makeNative = function() {
            var params = '';
            if (this.opts.autoplay) {
                params += '&autoplay=1';
            }

            this.$iframe = $('<iframe>').attr({
                src: ('//player.vimeo.com/video/' + this.opts.video + '?api=1' + params),
                frameborder: '0',
                webkitallowfullscreen: '',
                mozallowfullscreen: '',
                allowfullscreen: ''
            });
            this._containerHTML = this.$container.prop('outerHTML');
            this.$container.replaceWith(this.$iframe);

            if (!window.$f) {
                return this.raise('$f is undefined');
            }

            var that = this;
            this.native = $f(this.$iframe.get(0));
            this.native.addEvent('ready', function() {
                that.native.addEvent('play', function() {
                    that.trigger('play');
                });
                that.native.addEvent('pause', function() {
                    that.trigger('pause');
                });
                that.native.addEvent('finish', function() {
                    that.trigger('ended');
                });

                if (that.opts.autoplay) {
                    that.trigger('play');
                }
                that.trigger('ready');
            });
        };

        /*
            Начало воспроизведения
         */
        cls.play = function() {
            if (!this.native) {
                this.warn('not ready yet');
                return this;
            }

            this.native.api('play');
            return this;
        };

        /*
            Переход к точке воспроизведения
         */
        cls.position = function(value) {
            if (!this.native) {
                this.warn('not ready yet');
                return this;
            }

            if (typeof value != 'number') {
                this.error('value should be a number');
                return this;
            }

            this.native.api('seekTo', value);
            return this;
        };

        /*
            Пауза
         */
        cls.pause = function() {
            if (!this.native) {
                this.warn('not ready yet');
                return this;
            }

            this.native.api('pause');
            return this;
        };

        /*
            Остановка воспроизведения
         */
        cls.stop = function() {
            if (!this.native) {
                this.warn('not ready yet');
                return this;
            }

            this.native.api('unload');
            return this;
        };

        /*
            Установка уровня громкости
         */
        cls.volume = function(value) {
            if (!this.native) {
                this.warn('not ready yet');
                return this;
            }

            if (typeof value != 'number') {
                this.error('value should be a number');
                return this;
            }

            this.native.api('setVolume', value / 100);
            return this;
        };
    });


    var vimeo_ready = false;
    window.onVimeoAPIReady = function() {
        vimeo_ready = true;
        $(document).trigger('vimeo-ready');
    };

    $(document).ready(function() {
        var script = document.createElement('script');
        script.onload = onVimeoAPIReady;
        script.src = 'https://f.vimeocdn.com/js/froogaloop2.min.js';
        document.body.appendChild(script);
    });

    /*
        Выполнение callback, когда JS Vimeo загружен и готов
     */
    window.Vimeo.ready = function(callback) {
        if (vimeo_ready) {
            callback()
        } else {
            $(document).one('vimeo-ready', callback);
        }
    };

})(jQuery);
