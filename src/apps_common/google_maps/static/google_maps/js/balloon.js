(function($) {

    /*

     */
    window.GMapBalloon = Class(GMapOverlayBase, function GMapBalloon(cls, superclass) {
        cls.prototype.NATIVE_EVENTS = [
            'domready',
            'closeclick',
            'content_changed',
            'position_changed'
        ];

        /*
            Настройки по умолчанию
         */
        cls.prototype.getDefaultOpts = function() {
            return $.extend(superclass.prototype.getDefaultOpts.call(this), {
                content: '',
                position: null
            });
        };

        /*
            Инициализация
         */
        cls.prototype.onInit = function() {
            if (!this.opts.position) {
                return this.raise('position required');
            } else if (this.opts.position instanceof GMapPoint == false) {
                return this.raise('position should be a GMapPoint instance');
            }

            superclass.prototype.onInit.call(this);

            // точка
            this._position = this.opts.position;

            // состояние
            this.opened = false;
        };

        /*
            Вызывается при добавлении оверлея на карту
         */
        cls.prototype.onAdd = function() {
            this.$container = $('<div>').addClass('balloon');

            var panes = this.native.getPanes();
            panes[this.layer].appendChild(this.$container.get(0));
        };

        /*
            Отрисовка оверлея
         */
        cls.prototype.draw = function() {
            var projection = this.native.getProjection();
            var point = projection.fromLatLngToDivPixel(this.position());

            this.$container.css({
                left: point.x,
                top: point.y
            });
        };

        /*
            Вызывается при откреплении оверлея от карты
         */
        cls.prototype.onRemove = function() {
            this.$container.remove();
            this.$container = null;
        };

        /*
            Получение / установка положения
         */
        cls.prototype.position = function(value) {
            if (value === undefined) {
                // получение положения
                return this._position;
            }

            if (value) {
                if (value instanceof GMapPoint == false) {
                    this.error('value should be a GMapPoint instance');
                    return this;
                }

                this._position = value;
                //this.native.setPosition(value.native);
            }

            return this;
        };
    });

})(jQuery);
