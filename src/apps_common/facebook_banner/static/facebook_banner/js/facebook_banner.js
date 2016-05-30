(function($) {

    var APP_ID = window.js_storage.fb_banner_appid;
    var TIMEOUT = window.js_storage.fb_banner_timeout;

    /*
        Показ окна баннера
     */
    window.showFacebookBanner = function() {
        return $.ajax({
            url: window.js_storage.fb_banner_url,
            type: 'GET',
            dataType: 'json',
            success: function(response) {
                if (response.html) {
                    $('#facebook-banner').remove();
                    $(document.body).append(response.html);

                    // Добавление Facebook SDK
                    (function(d, s, id) {
                        var js, fjs = d.getElementsByTagName(s)[0];
                        if (d.getElementById(id)) return;
                        js = d.createElement(s);
                        js.id = id;
                        js.onload = function() {
                            setTimeout(function() {
                                $('#facebook-banner').fadeIn(300);
                            }, 1000);
                        };
                        js.src = "//connect.facebook.net/ru_RU/sdk.js#xfbml=1&version=v2.4&appId=" + APP_ID;
                        fjs.parentNode.insertBefore(js, fjs);
                    }(document, 'script', 'facebook-jssdk'));
                }
            }
        });
    };

    $(document).on('click', '#facebook-banner .close-button', function() {
        $('#facebook-banner').fadeOut(300, function() {
            $(this).remove()
        });
        $.cookie('fb-banner-shown', 1, {
            expires: 30,
            path: '/'
        });
    });

    $(document).ready(function() {
        if ($.cookie('fb-banner-shown')) {
            return
        }

        if ($.winWidth() < 640) {
            return
        }

        setTimeout(showFacebookBanner, TIMEOUT - 1000);
    })

})(jQuery);