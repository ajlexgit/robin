(function($) {

    // ==================================
    //  Авторизация
    // ==================================

    /*
        Показ окна авторизации
     */
    window.loginPopup = function() {
        $.preloader();

        return $.ajax({
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
    };

    $(document).on('click', '.login-popup', function() {
        // Открытие окна авторизации
        loginPopup();
        return false;
    }).on('submit', '#ajax-login-form', function() {
        // Отправка Ajax-формы авторизации
        var form = $(this);
        $.preloader();

        $.ajax({
            url: window.js_storage.ajax_login,
            type: 'POST',
            data: form.serialize(),
            dataType: 'json',
            success: function(response) {
                if (response.errors) {
                    // ошибки формы
                    $.popup({
                        classes: 'users-popup',
                        content: response.form
                    }).show();
                } else {
                    $(document).trigger('login.auth.users', response);
                    $('input[name="csrfmiddlewaretoken"]').val($.cookie('csrftoken'));
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


    // ==================================
    //  Регистрация
    // ==================================

    /*
        Показ окна регистрации
     */
    window.registerPopup = function() {
        $.preloader();

        return $.ajax({
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
    };

    $(document).on('click', '.register-popup', function() {
        // Открытие окна регистрации
        registerPopup();
        return false;
    }).on('submit', '#ajax-register-form', function() {
        // Отправка Ajax-формы регистрации
        var form = $(this);
        $.preloader();

        $.ajax({
            url: window.js_storage.ajax_register,
            type: 'POST',
            data: form.serialize(),
            dataType: 'json',
            success: function(response) {
                if (response.errors) {
                    // ошибки формы
                    $.popup({
                        classes: 'users-popup',
                        content: response.form
                    }).show();
                } else {
                    $(document).trigger('register.auth.users', response);
                    $(document).trigger('login.auth.users', response);
                    $('input[name="csrfmiddlewaretoken"]').val($.cookie('csrftoken'));
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

    // ==================================
    //  Сброс пароля
    // ==================================

    /*
        Показ окна смены пароля. Этап ввода email (для не авторизованных юзеров)
     */
    window.resetPasswordPopup = function() {
        $.preloader();

        return $.ajax({
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
    };

    $(document).on('click', '.reset-password-popup', function() {
        // Открытие окна сброса пароля
        resetPasswordPopup();
        return false;
    }).on('submit', '#ajax-reset-password-form', function() {
        // Отправка Ajax-формы сброса пароля
        var form = $(this);
        $.preloader();

        $.ajax({
            url: window.js_storage.ajax_reset,
            type: 'POST',
            data: form.serialize(),
            dataType: 'json',
            success: function(response) {
                if (response.errors) {
                    // ошибки формы
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


    /*
        Показ окна смены пароля. Этап ввода нового пароля (для авторизованных юзеров)
     */
    window.resetConfirmPopup = function() {
        $.preloader();

        return $.ajax({
            url: window.js_storage.ajax_reset_confirm,
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
    };

    $(document).on('click', '.reset-confirm-popup', function() {
        // Открытие окна установки пароля
        resetConfirmPopup();
        return false;
    }).on('submit', '#ajax-reset-confirm-form', function() {
        // Отправка Ajax-формы установки пароля
        var form = $(this);
        $.preloader();

        $.ajax({
            url: window.js_storage.ajax_reset_confirm,
            type: 'POST',
            data: form.serialize(),
            dataType: 'json',
            success: function(response) {
                if (response.errors) {
                    // ошибки формы
                    $.popup({
                        classes: 'users-popup',
                        content: response.form
                    }).show();
                } else {
                    $(document).trigger('reset-confirm.auth.users');
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


    // ==================================
    //  Выход из профиля
    // ==================================

    window.logoutPopup = function() {
        $.preloader();

        return $.ajax({
            url: window.js_storage.ajax_logout,
            type: 'POST',
            dataType: 'json',
            success: function(response) {
                $(document).trigger('logout.auth.users', response);
                $('input[name="csrfmiddlewaretoken"]').val($.cookie('csrftoken'));
                $.popup().hide();
            },
            error: function() {
                alert(gettext('Connection error'));
                $.popup().hide();
            }
        });
    };

    $(document).on('click', '.logout', function() {
        logoutPopup();
        return false;
    });

})(jQuery);
