(function($) {

    /*
        https://developers.google.com/youtube/iframe_api_reference?hl=ru

        Требует:
            jquery.utils.js

        Параметры:
            video       - строка с ключем видео
            lang        - язык плеера. По умолчанию - аттрибут lang <html>
            start       - позиция начала воспроизведения. В секундах от начала.
            end         - позиция конца воспроизведения. В секундах от начала.
            loop        - зациклить видео
            relative    - показать похожие видео после окончания
            autoplay    - автоматически начать показ

        Пример:
            <div id="player"></div>

            <script>
                var player = YouTube('#player', {
                    video: 'Ssk5JQ768qg'
                }).on('ready', function() {
                    // начало воспроизведения с середины
                    var duration = this.getDuration();
                    this.position(duration / 2);
                    this.play();
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

                // загрузка другого видео
                player.loadVideo('0cLvWmuhY5E');
            </script>
    */

    window.YouTube = Class(EventedObject, function YouTube(cls, superclass) {
        cls.defaults = {
            video: '',
            lang: '',
            start: null,
            end: null,
            loop: false,
            relative: false,
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
            window.YouTube.ready(function() {
                that.makeNative();
            });
        };

        /*
            Освобождение ресурсов
         */
        cls.destroy = function() {
            this.stop();
            if (this.native) {
                this.native.destroy();
                this.native = null;
            }
            superclass.destroy.call(this);
        };

        /*
            Создание нативного объекта
         */
        cls.makeNative = function() {
            var playerVars = {
                autoplay: this.opts.autoplay,
                hl: this.opts.lang,
                loop: this.opts.loop,
                rel: this.opts.relative
            };
            if (this.opts.start && (typeof this.opts.start == 'number')) {
                playerVars.start = this.opts.start;
            }
            if (this.opts.end && (typeof this.opts.end == 'number')) {
                playerVars.end = this.opts.end;
            }
            if (this.opts.loop) {
                playerVars.playlist = this.opts.video;
            }
            if (!this.opts.lang) {
                var default_lang = document.documentElement.getAttribute('lang');
                if (default_lang) {
                    playerVars.hl = default_lang;
                }
            }

            if (!window.YT) {
                return this.raise('YT is undefined');
            }

            var that = this;
            this.native = new YT.Player(this.$container.get(0), {
                videoId: this.opts.video,
                playerVars: playerVars,
                events: {
                    onReady: function() {
                        that.trigger('ready');
                    }
                }
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

            this.native.playVideo();
            return this;
        };

        /*
            Получение / переход к точке воспроизведения
         */
        cls.position = function(value) {
            if (!this.native) {
                this.warn('not ready yet');
                return this;
            }

            if (value === undefined) {
                return this.native.getCurrentTime();
            }

            if (typeof value != 'number') {
                this.error('value should be a number');
                return this;
            }

            this.native.seekTo(value);
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

            this.native.pauseVideo();
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

            this.native.stopVideo();
            return this;
        };

        /*
            Получение / включение / выключение звука
         */
        cls.mute = function(value) {
            if (!this.native) {
                this.warn('not ready yet');
                return this;
            }

            if (value === undefined) {
                return this.native.isMuted();
            }

            if (value) {
                this.native.mute();
            } else {
                this.native.unMute();
            }

            return this;
        };

        /*
            Получение / установка уровня громкости
         */
        cls.volume = function(value) {
            if (!this.native) {
                this.warn('not ready yet');
                return this;
            }

            if (value === undefined) {
                return this.native.getVolume();
            }

            if (typeof value != 'number') {
                this.error('value should be a number');
                return this;
            }

            this.native.setVolume(value);
            return this;
        };

        /*
            Получение продолжительности видео
         */
        cls.getDuration = function() {
            if (!this.native) {
                this.warn('not ready yet');
                return this;
            }

            return this.native.getDuration();
        };

        /*
            Получение ссылки на видео
         */
        cls.getVideoUrl = function() {
            if (!this.native) {
                this.warn('not ready yet');
                return this;
            }

            return this.native.getVideoUrl();
        };

        /*
            Загрузка другого видео по его идентификатору
         */
        cls.loadVideo = function(videoId) {
            if (!this.native) {
                this.warn('not ready yet');
                return this;
            }

            this.native.loadVideoById(videoId);
            return this;
        };
    });


    var youtube_ready = false;
    window.onYouTubeIframeAPIReady = function() {
        youtube_ready = true;
        $(document).trigger('youtube-ready');
    };

    $(document).ready(function() {
        var script = document.createElement('script');
        script.src = 'https://www.youtube.com/iframe_api';
        document.body.appendChild(script);
    });

    /*
        Выполнение callback, когда JS Youtube загружен и готов
     */
    window.YouTube.ready = function(callback) {
        if (youtube_ready) {
            callback()
        } else {
            $(document).one('youtube-ready', callback);
        }
    };

})(jQuery);
