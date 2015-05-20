(function($) {

    window.Comments = function($wrapper, options) {
        var settings = $.extend({
            comment_class: 'comment',
            comments_container_class: 'comments',
            form_container_class: 'comments-form-wrapper',
            reply_template_class: 'comments-reply-template',
            edit_template_class: 'comments-edit-template'
        }, options);

        var that = this;
        var content_type = $wrapper.data('content_type');
        var object_id = $wrapper.data('object_id');
        var $reply_form_template = $wrapper.find('.' + settings.reply_template_class).html();
        var $edit_form_template = $wrapper.find('.' + settings.edit_template_class).html();

        /*
            Возвращает jQuery-список, содержащий ветку комментариев
        */
        var getBranch = function($parent_comment) {
            var parent_comment_level = $parent_comment.data('level');
            return $parent_comment.nextUntil(function() {
                var self = $(this);
                return !self.hasClass(settings.comment_class) || self.data('level') <= parent_comment_level;
            }).addBack();
        };

        /*
            Удаление всех пустых форм
        */
        this.removeEmptyForms = function() {
            $wrapper.find('.' + settings.comments_container_class + ' form').each(function() {
                var $form = $(this);
                if (!$form.find('textarea').val()) {
                    $form.remove();
                }
            });
        };

        /*
            Обновление всего блока комментариев
        */
        this.refresh = function() {
            var df = $.Deferred();
            $.ajax({
                url: window.js_storage.comments_refresh,
                type: 'GET',
                data: {
                    'content_type': content_type,
                    'object_id': object_id
                },
                dataType: 'json',
                success: function(response) {
                    $wrapper.find('.' + settings.comments_container_class).replaceWith(response.comments);
                    $wrapper.find('.' + settings.form_container_class).replaceWith(response.initial_form);
                    df.resolve();
                },
                error: function() {
                    df.reject(window.Comments.ajax_error);
                }
            });
            return df.promise();
        };

        /*
            Показ формы ответа на коммент
        */
        this.replyForm = function($comment) {
            var df = $.Deferred();
            this.removeEmptyForms();
            $comment.find('form').remove();
            var $reply_form = $($reply_form_template);
            $reply_form.find('input[name="parent"]').val($comment.data('id'));
            $comment.append($reply_form);
            $reply_form.find('textarea').keyup().focus();
            return df.resolve($reply_form);
        };

        /*
            Показ формы редактирования комментария
        */
        this.editForm = function($comment) {
            var df = $.Deferred();
            $.ajax({
                url: window.js_storage.comment_change,
                type: 'GET',
                data: {
                    'content_type': content_type,
                    'object_id': object_id,
                    'comment': $comment.data('id')
                },
                success: function(response) {
                    if (response.error) {
                        return df.reject(response.error);
                    }
                    that.removeEmptyForms();
                    $comment.find('form').remove();
                    var $edit_form = $($edit_form_template);
                    $comment.append($edit_form);
                    $edit_form.find('textarea').val(response.text).keyup().focus();
                    df.resolve($edit_form);
                },
                error: function() {
                    df.reject(window.Comments.ajax_error);
                }
            });
            return df.promise();
        };

        /*
            Удаление комментария
        */
        this.remove = function($comment) {
            var df = $.Deferred();
            $.ajax({
                url: window.js_storage.comment_delete,
                type: 'POST',
                data: {
                    'content_type': content_type,
                    'object_id': object_id,
                    'comment': $comment.data('id')
                },
                dataType: 'json',
                success: function(response) {
                    if (response.error) {
                        return df.reject(response.error);
                    }
                    var $new_comment = $(response.html);
                    $comment.replaceWith($new_comment);
                    df.resolve($new_comment);
                },
                error: function() {
                    df.reject(window.Comments.ajax_error);
                }
            });
            return df.promise();
        };

        /*
            Восстановление комментария
        */
        this.restore = function($comment) {
            var df = $.Deferred();
            $.ajax({
                url: window.js_storage.comment_restore,
                type: 'POST',
                data: {
                    'content_type': content_type,
                    'object_id': object_id,
                    'comment': $comment.data('id')
                },
                dataType: 'json',
                success: function(response) {
                    if (response.error) {
                        return df.reject(response.error);
                    }
                    var $new_comment = $(response.html);
                    $comment.replaceWith($new_comment);
                    df.resolve($new_comment);
                },
                error: function() {
                    df.reject(window.Comments.ajax_error);
                }
            });
            return df.promise();
        };

        /*
            Оценка комментария
        */
        this.vote = function($comment, is_like) {
            var df = $.Deferred();
            $.ajax({
                url: window.js_storage.comment_vote,
                type: 'POST',
                data: {
                    'content_type': content_type,
                    'object_id': object_id,
                    'comment': $comment.data('id'),
                    'is_like': Number(is_like)
                },
                dataType: 'json',
                success: function(response) {
                    if (response.error) {
                        return df.reject(response.error);
                    }
                    var $new_comment = $(response.html);
                    $comment.replaceWith($new_comment);
                    df.resolve($new_comment);
                },
                error: function() {
                    df.reject(window.Comments.ajax_error);
                }
            });
            return df.promise();
        };

        /*
            Добавление комментария
        */
        this.post = function($form) {
            var df = $.Deferred();
            $.ajax({
                url: window.js_storage.comment_post,
                type: 'POST',
                data: $form.serialize(),
                success: function(response) {
                    if (response.error) {
                        return df.reject(response.error);
                    }
                    var $comment = $(response.html),
                        $parent_comment = $form.closest('.' + settings.comment_class);
                    if ($parent_comment.length) {
                        // ответ на коммент
                        $form.remove();
                        getBranch($parent_comment).last().after($comment);
                    } else {
                        // добавление корневого коммента
                        $wrapper.find('.' + settings.comments_container_class).append($comment);
                        $form.find('textarea').val('').keyup();
                    }
                    df.resolve($comment, $parent_comment);
                },
                error: function() {
                    df.reject(window.Comments.ajax_error);
                }
            });
            return df.promise();
        };

        /*
            Редактирование комментария
        */
        this.edit = function($form) {
            var df = $.Deferred();
            var $comment = $form.closest('.' + settings.comment_class);
            var formData = $form.serializeArray();
            formData.push({
                name: 'comment',
                value: $comment.data('id')
            });

            $.ajax({
                url: window.js_storage.comment_change,
                type: 'POST',
                data: formData,
                success: function(response) {
                    if (response.error) {
                        return df.reject(response.error);
                    }
                    var $new_comment = $(response.html);
                    $comment.replaceWith($new_comment);
                    df.resolve($new_comment);
                },
                error: function() {
                    df.reject(window.Comments.ajax_error);
                }
            });
            return df.promise();
        };

        // Удаляем атрибуты, чтобы лишний раз не палить
        $wrapper.removeAttr('data-content_type data-object_id');

        // Сохраняем объект в DOM-элементе
        $wrapper.data('object', this);
    };

    window.Comments.ajax_error = 'Ошибка соединения с сервером';

})(jQuery);