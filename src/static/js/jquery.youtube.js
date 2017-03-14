(function($) {
    'use strict';

    /*
        https://developers.google.com/youtube/iframe_api_reference?hl=ru

        Требует:
            jquery.utils.js

        Параметры:
            video       - строка с ключем видео

            + любые из документации:
                https://developers.google.com/youtube/player_parameters?playerVersion=HTML5&hl=ru

        События:
            // Видео готово к воспроизведению
            ready

            // Видео начало воспроизводиться
            play

            // Изменилась позиция видео
            timeupdate

            // Видео перестало воспроизводиться
            pause

            // Видео закончилось
            end

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
            video: ''
        };

        // интервал проверки времени воспроизведения
        cls.CHECK_POSITION_TIMEOUT = 100;

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
                this.$iframe = null;
                this.native = null;
            }
            superclass.destroy.call(this);
        };

        /*
            Создание нативного объекта
         */
        cls.makeNative = function() {
            if (!window.YT) {
                return this.raise('YT is undefined');
            }

            // копирование в playerVars всех свойств, кроме тех,
            // что указаны в defaults.
            var playerVars = {};
            for (var key in this.opts) {
                if (!this.opts.hasOwnProperty(key)) continue;
                if (key in this.defaults) continue;
                playerVars[key] = this.opts[key]
            }

            // форматирование
            if ('autoplay' in playerVars) {
                playerVars.autoplay = Number(Boolean(playerVars.autoplay));
            }

            if ('controls' in playerVars) {
                playerVars.controls = Number(playerVars.controls);
            }

            if ('disablekb' in playerVars) {
                playerVars.disablekb = Number(Boolean(playerVars.disablekb));
            }

            if ('showinfo' in playerVars) {
                playerVars.showinfo = Number(Boolean(playerVars.showinfo));
            }

            if (!('hl' in playerVars)) {
                playerVars.hl = document.documentElement.getAttribute('lang') || 'en';
            }

            var that = this;
            this.native = new YT.Player(this.$container.get(0), {
                videoId: this.opts.video,
                playerVars: playerVars,
                events: {
                    onReady: function(event) {
                        that.$iframe = $(event.target.getIframe());
                        that.trigger('ready');
                    },
                    onStateChange: function(event) {
                        var code = event.data;
                        if (code == YT.PlayerState.UNSTARTED) {
                            that.stopInteraval();
                        } else if (code == YT.PlayerState.BUFFERING) {

                        } else if (code == YT.PlayerState.PLAYING) {
                            that.startInteraval();
                            that.trigger('play');
                        } else if (code == YT.PlayerState.PAUSED) {
                            that.stopInteraval();
                            that.trigger('pause');
                        } else if (code == YT.PlayerState.ENDED) {
                            that.stopInteraval();
                            that.trigger('pause');
                            that.trigger('end');
                        }
                    }
                }
            });
        };

        /*
            Создание таймера, проверяющего позицию видео
         */
        cls.startInteraval = function() {
            this.stopInteraval();
            this._currentTime = -1;
            this._timer = setInterval($.proxy(this.updateTime, this), this.CHECK_POSITION_TIMEOUT);
        };

        /*
            Остановка таймера, проверяющего позицию видео
         */
        cls.stopInteraval = function() {
            if (this._timer) {
                clearInterval(this._timer);
                this._timer = null;
            }
        };

        cls.updateTime = function() {
            if (!this.native) {
                return;
            }

            var time = parseInt(this.position()) || 0;
            if (time != this._currentTime) {
                this._currentTime = time;
                this.trigger('timeupdate', time);
            }
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

            this.stopInteraval();
            this.trigger('pause');

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
