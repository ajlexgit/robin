(function($) {

    /*
        Класс наложения картинки на карту Google в трех экземплярах.
        Дополнительные копии нужны на низком зуме из-за косячности определения
        координат картой.

        Координаты coords ДОЛЖНЫ описывать вертикальную черту (lng1 == lng2)
     */
    window.GMapImageTripleOverlay = Class(GMapOverlayBase, function GMapImageTripleOverlay(cls, superclass) {
        /*
            Настройки по умолчанию
         */
        cls.prototype.getDefaultOpts = function() {
            return $.extend(superclass.prototype.getDefaultOpts.call(this), {
                src: '',
                coords: {
                    topright: null,
                    bottomleft: null
                }
            });
        };

        /*
            Вызывается при добавлении оверлея на карту
         */
        cls.prototype.onInit = function() {
            if (!this.opts.src) {
                return this.raise('src required');
            }

            if (!this.opts.coords) {
                return this.raise('coords required');
            } else if (this.opts.coords.bottomleft instanceof GMapPoint == false) {
                return this.raise('coords.bottomleft should be a GMapPoint instance');
            } else if (this.opts.coords.topright instanceof GMapPoint == false) {
                return this.raise('coords.topright should be a GMapPoint instance');
            } else {
                this.bounds = new google.maps.LatLngBounds(
                    this.opts.coords.bottomleft.native,
                    this.opts.coords.topright.native
                )
            }

            superclass.prototype.onInit.call(this);
        };

        /*
            Вызывается при добавлении оверлея на карту
         */
        cls.prototype.onAdd = function() {
            this.$container = $('<div>').css({
                position: 'absolute',
                minWidth: '1px'
            });

            this.$img = $('<img>', {
                src: this.opts.src
            }).addClass('center-copy').css({
                position: 'absolute',
                left: 0,
                top: 0,
                height: '100%'
            });

            this.$left = this.$img.clone().addClass('right-copy');
            this.$right = this.$img.clone().addClass('right-copy');

            this.$container.append(this.$left, this.$img, this.$right);

            // Add the element to the "overlayLayer" pane.
            var panes = this.native.getPanes();
            panes[this.layer].appendChild(this.$container.get(0));
        };

        /*
            Отрисовка оверлея
         */
        cls.prototype.draw = function() {
            var overlayProjection = this.native.getProjection();

            var bottomleft = this.bounds.getSouthWest();
            var righttop = this.bounds.getNorthEast();
            var sw = overlayProjection.fromLatLngToDivPixel(bottomleft);
            var ne = overlayProjection.fromLatLngToDivPixel(righttop);

            this.$container.css({
                left: sw.x,
                top: ne.y,
                height: Math.abs(sw.y - ne.y)
            });

            // левая и правая копии
            var worldWidth = overlayProjection.getWorldWidth();
            this.$left.css({
                left: -worldWidth
            });
            this.$right.css({
                left: worldWidth
            });
        };

        /*
            Вызывается при откреплении оверлея от карты
         */
        cls.prototype.onRemove = function() {
            this.$container.remove();
            this.$container = null;
        };
    });

})(jQuery);
