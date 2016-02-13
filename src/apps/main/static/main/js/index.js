(function($) {

    $(document).ready(function() {

        WinHeightSlider('.section-slider .slider', {
            loop: true,
            itemSelector: '.slider-item'
        }).attachPlugins([
            SliderSideAnimation({}),
            SliderSideShortestAnimation({}),
            SliderFadeAnimation({}),
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
        $('#gallery').find('.item').on('click', function() {
            $.gallery({
                previews: '#gallery .item',
                activePreview: this
            });
        });
    });

})(jQuery);
