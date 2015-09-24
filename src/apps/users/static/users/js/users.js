(function($) {
    /*
        Открытие окна регистрации
    */
    $(document).on('click', '.register-popup', function() {
        $.preloader();

        $.ajax({
            url: window.js_storage.ajax_register,
            type: 'GET',
            success: function(response) {
                $.popup({
                    classes: 'users-popup',
                    content: response
                }).show();
            },
            error: function() {
                alert(gettext('Connection error'));
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
        $.preloader();

        $.ajax({
            url: window.js_storage.ajax_register,
            type: 'POST',
            data: form.serialize(),
            dataType: 'json',
            success: function(response) {
                if (response.form) {
                    $.popup({
                        classes: 'users-popup',
                        content: response.form
                    }).show();
                } else {
                    $(document).trigger('register.auth.users', response);
                    $(document).trigger('login.auth.users', response);
                    $.popup().hide();
                }
            },
            error: function() {
                alert(gettext('Connection error'));
                $.popup().hide();
            }
        });
        return false;
    });


    /*
        Открытие окна авторизации
    */
    $(document).on('click', '.login-popup', function() {
        $.preloader();

        $.ajax({
            url: window.js_storage.ajax_login,
            type: 'GET',
            success: function(response) {
                $.popup({
                    classes: 'users-popup',
                    content: response
                }).show();
            },
            error: function() {
                alert(gettext('Connection error'));
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
        $.preloader();

        $.ajax({
            url: window.js_storage.ajax_login,
            type: 'POST',
            data: form.serialize(),
            dataType: 'json',
            success: function(response) {
                if (response.form) {
                    $.popup({
                        classes: 'users-popup',
                        content: response.form
                    }).show();
                } else {
                    $(document).trigger('login.auth.users', response);
                    $.popup().hide();
                }
            },
            error: function() {
                alert(gettext('Connection error'));
                $.popup().hide();
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
                $(document).trigger('logout.auth.users', response);
            },
            error: function() {
                alert(gettext('Connection error'));
                $.popup().hide();
            }
        });
        return false;
    });


    /*
        Открытие окна сброса пароля
    */
    $(document).on('click', '.reset-password-popup', function() {
        $.preloader();

        $.ajax({
            url: window.js_storage.ajax_reset,
            type: 'GET',
            success: function(response) {
                $.popup({
                    classes: 'users-popup',
                    content: response
                }).show();
            },
            error: function() {
                alert(gettext('Connection error'));
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
        $.preloader();

        $.ajax({
            url: window.js_storage.ajax_reset,
            type: 'POST',
            data: form.serialize(),
            dataType: 'json',
            success: function(response) {
                if (response.form) {
                    $.popup({
                        classes: 'users-popup',
                        content: response.form
                    }).show();
                } else {
                    $(document).trigger('reset-password.auth.users');
                    $.popup({
                        classes: 'users-popup',
                        content: response.done
                    });
                }
            },
            error: function() {
                alert(gettext('Connection error'));
                $.popup().hide();
            }
        });
        return false;
    });

})(jQuery);
