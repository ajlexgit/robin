(function($) {

    $(document).ready(function() {

        Slider('.section-slider .slider', {
            loop: true,
            itemSelector: '.slider-item'
        }).attachPlugins([
            SliderSideAnimation({}),
            SliderSideShortestAnimation({}),
            SliderDragPlugin({}),
            SliderControlsPlugin({
                animationName: 'side-shortest'
            }),
            SliderNavigationPlugin({
                animationName: 'side',
                container: '.slider-list-wrapper'
            })
        ]);

        // gallery popup
        $(document).on('click', '#gallery .slider-item', function() {
            $.gallery({
                previews: '#gallery .slider-item',
                activePreview: this
            });
        });

        // gallery slider
        Slider('#gallery .slider', {
            loop: false,
            itemsPerSlide: function() {
                var winWidth = $.winWidth();
                if (winWidth >= 1024) {
                    return 4;
                } else if (winWidth >= 640) {
                    return 3;
                } else if (winWidth >= 400) {
                    return 2;
                } else {
                    return 1;
                }
            }
        }).attachPlugins([
            SliderSideAnimation({
                margin: 20
            }),
            SliderSideShortestAnimation({
                margin: 20
            }),
            SliderDragPlugin({
                margin: 20
            }),
            SliderControlsPlugin({
                animationName: 'side-shortest'
            })
        ]).on('after_set_ips', function(ips) {
            // сохранение текущего значения
            this._ips = ips;
        }).on('resize', function() {
            // обновление, если значение изменилось
            var itemsPerSlide = this.opts.itemsPerSlide.call(this);
            if (this._ips != itemsPerSlide) {
                this.setItemsPerSlide(itemsPerSlide);
            }
        });
    });

})(jQuery);
