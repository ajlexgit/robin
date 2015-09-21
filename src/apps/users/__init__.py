"""
    Модуль пользователей.

    Содержит каркас обработки стандартных событий (авторизация, регистрация и т.п.).
    Модель пользователя - кастомная: добавлен аватар.

    Встроенный JS-файл users.js генерирует события на $(document), чтобы можно было
    навесить дополнительныое поведение после авторизации/регитрации/т.п:

        $(document).on('register.auth', function(e, response) {
            alert('You have been registered successfully!');
        });

"""

default_app_config = 'users.apps.Config'
