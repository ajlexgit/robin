(function() {

    var loadJS = function(src, async) {
        var script = document.createElement('script');
        script.src = src;
        script.async = async || false;
        document.body.appendChild(script);
    };

    if (!Modernizr.es5) {
        loadJS("/static/polyfills/es5-shim.min.js");
    }

    if (!Modernizr.flexbox) {
        loadJS("/static/polyfills/respond.min.js");
    }

    if (!Modernizr.svg) {
        loadJS("/static/polyfills/svg2png.js");
    }

})();