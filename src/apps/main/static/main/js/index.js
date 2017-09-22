//======================
//         First slider
//----------------------
(function($) {

    $(document).ready(function() {

        Slider('#main-slider .slider', {
                sliderHeight: Slider.prototype.HEIGHT_CURRENT,
                loop: false,
                itemsPerSlide: 1
            }).attachPlugins([
                SliderSideAnimation({
                    margin: 20
                }),
                SliderSideShortestAnimation({
                    margin: 20
                }),
                SliderFadeAnimation(),
                SliderControlsPlugin({
                    animationName: 'side-shortest'
                }),
                SliderNavigationPlugin({
                    animationName: 'side'
                }),
                SliderDragPlugin({
                    margin: 20
                }),
                SliderAutoscrollPlugin({
                    animationName: 'fade',
                    direction: 'random',
                    interval: 6000
                                
                
                })
            ]);


    });

})(jQuery);


//=======================
//         second slider
//-----------------------
(function($) {

    $(document).ready(function() {

        Slider('#testi-slider .testi-slider', {
                sliderHeight: Slider.prototype.HEIGHT_CURRENT,
                loop: false,
                itemsPerSlide: 2
            }).attachPlugins([
                SliderSideAnimation({
                    margin: 20
                }),
                SliderSideShortestAnimation({
                    margin: 20
                }),
                SliderFadeAnimation(),
                SliderControlsPlugin({
                    animationName: 'side-shortest'
                }),
                SliderNavigationPlugin({
                    animationName: 'side'
                    
                }),
                SliderDragPlugin({
                    margin: 20
                }),
                SliderAutoscrollPlugin({
                    animationName: 'fade',
                    direction: 'random',
                    interval: 6000
                                
                
                })
            ]);


    });

})(jQuery);
