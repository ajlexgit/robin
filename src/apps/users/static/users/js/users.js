(function($) {
    /*
        Открытие окна регистрации
    */
    $(document).on('click', '.register-popup', function() {
        $.popup.force({
            classes: 'preloader',
            ui: false,
            outClick: false
        });

        $.ajax({
            url: window.js_storage.ajax_register,
            type: 'GET',
            success: function(response) {
                $.popup({
                    classes: 'popup-auth',
                    content: response
                });
            },
            error: function() {
                $.popup().hide();
            }
        });
        return false;
    });

    /*
        AJAX register
    */
    $(document).on('submit', '#ajax-register-form', function() {
        var form = $(this);
        $.popup.force({
            classes: 'preloader',
            ui: false,
            outClick: false
        });
        $.ajax({
            url: window.js_storage.ajax_register,
            type: 'POST',
            data: form.serialize(),
            dataType: 'json',
            success: function(response) {
                if (response.errors) {
                    $.popup({
                        classes: 'popup-auth',
                        content: response.errors
                    });
                } else {
                    $(document).trigger('register.auth', response);
                    $(document).trigger('login.auth', response);
                    $.popup().hide();
                }
            },
            error: function() {
                alert(gettext('Connection error'));
            },
            complete: function() {
                $.popup().update({
                    classes: 'popup-auth'
                });
            }
        });
        return false;
    });


    /*
        Открытие окна авторизации
    */
    $(document).on('click', '.login-popup', function() {
        $.popup.force({
            classes: 'preloader',
            ui: false,
            outClick: false
        });
        $.ajax({
            url: window.js_storage.ajax_login,
            type: 'GET',
            success: function(response) {
                $.popup({
                    classes: 'popup-auth',
                    content: response
                });
            },
            error: function() {
                $.popup().hide();
            }
        });
        return false;
    });


    /*
        AJAX login
    */
    $(document).on('submit', '#ajax-login-form', function() {
        var form = $(this);
        $.popup.force({
            classes: 'preloader',
            ui: false,
            outClick: false
        });
        $.ajax({
            url: window.js_storage.ajax_login,
            type: 'POST',
            data: form.serialize(),
            dataType: 'json',
            success: function(response) {
                if (response.errors) {
                    $.popup({
                        classes: 'popup-auth',
                        content: response.errors
                    });
                } else {
                    $(document).trigger('login.auth', response);
                    $.popup().hide();
                }
            },
            error: function() {
                alert(gettext('Connection error'));
            },
            complete: function() {
                $.popup().update({
                    classes: 'popup-auth'
                });
            }
        });
        return false;
    });


    /*
        AJAX logout
    */
    $(document).on('click', '.logout', function() {
        var form = $(this).closest('form');
        $.ajax({
            url: window.js_storage.ajax_logout,
            type: 'POST',
            data: form.serialize(),
            dataType: 'json',
            success: function(response) {
                $(document).trigger('logout.auth', response);
            },
            error: function() {
                alert(gettext('Connection error'));
            }
        });
        return false;
    });


    /*
        Открытие окна сброса пароля
    */
    $(document).on('click', '.reset-password-popup', function() {
        $.popup.force({
            classes: 'preloader',
            ui: false,
            outClick: false
        });
        $.ajax({
            url: window.js_storage.ajax_reset,
            type: 'GET',
            success: function(response) {
                $.popup({
                    classes: 'popup-auth',
                    content: response
                });
            },
            error: function() {
                $.popup().hide();
            }
        });
        return false;
    });


    /*
        AJAX reset password
    */
    $(document).on('submit', '#ajax-reset-password-form', function() {
        var form = $(this);
        $.popup.force({
            classes: 'preloader',
            ui: false,
            outClick: false
        });
        $.ajax({
            url: window.js_storage.ajax_reset,
            type: 'POST',
            data: form.serialize(),
            dataType: 'json',
            success: function(response) {
                if (response.errors) {
                    $.popup({
                        classes: 'popup-auth',
                        content: response.errors
                    });
                } else {
                    $(document).trigger('reset.auth');
                    $.popup({
                        classes: 'popup-auth',
                        content: response.done
                    });
                }
            },
            error: function() {
                alert(gettext('Connection error'));
            },
            complete: function() {
                $.popup().update({
                    classes: 'popup-auth'
                });
            }
        });
        return false;
    });


    /*
        События
    */
    $(document).on('register.auth', function(e, response) {
        $('#auth-block').replaceWith(response.auth_block);
    }).on('reset.auth', function(e) {

    }).on('login.auth', function(e, response) {
        $('#auth-block').replaceWith(response.auth_block);
    }).on('logout.auth', function(e, response) {
        $('#auth-block').replaceWith(response.auth_block);
    });

})(jQuery);
