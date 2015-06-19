(function ($) {

    window.Comments = (function() {
        function Comments($wrapper, options) {
            this.settings = $.extend({
                comment_class: 'comment',
                comments_container_class: 'comments',
                form_container_class: 'comments-form-wrapper',
                reply_template_class: 'comments-reply-template',
                edit_template_class: 'comments-edit-template'
            }, options);

            this.$wrapper = $wrapper;
            this.content_type = $wrapper.data('content_type');
            this.object_id = $wrapper.data('object_id');
            this.$reply_form_template = $wrapper.find('.' + this.settings.reply_template_class).html();
            this.$edit_form_template = $wrapper.find('.' + this.settings.edit_template_class).html();

            // Удаляем атрибуты, чтобы лишний раз не палить
            $wrapper.removeAttr('data-content_type data-object_id');

            // Сохраняем объект в DOM-элементе
            $wrapper.data('object', this);
        }

        Comments.prototype.ajaxError = function(xhr, status, text) {
            return gettext('Ошибка соединения с сервером: ' + text);
        };

        /*
            Возвращает jQuery-список, содержащий ветку комментариев
        */
        Comments.prototype.getBranch = function($parent_comment) {
            var that = this;
            var parent_comment_level = $parent_comment.data('level');
            return $parent_comment.nextUntil(function() {
                var $self = $(this);
                return !$self.hasClass(that.settings.comment_class) || $self.data('level') <= parent_comment_level;
            }).addBack();
        };

        /*
            Удаление всех пустых форм
        */
        Comments.prototype.removeEmptyForms = function() {
            this.$wrapper.find('.' + this.settings.comments_container_class + ' form').each(function() {
                var $form = $(this);
                if (!$form.find('textarea').val()) {
                    $form.remove();
                }
            });
        };

        /*
            Обновление всего блока комментариев
        */
        Comments.prototype.refresh = function() {
            var that = this;
            var df = $.Deferred();
            $.ajax({
                url: window.js_storage.comments_refresh,
                type: 'GET',
                data: {
                    content_type: that.content_type,
                    object_id: that.object_id
                },
                dataType: 'json',
                success: function(response) {
                    that.$wrapper.find('.' + that.settings.comments_container_class).replaceWith(response.comments);
                    that.$wrapper.find('.' + that.settings.form_container_class).replaceWith(response.initial_form);
                    df.resolve();
                },
                error: function(xhr, status, text) {
                    df.reject(that.ajaxError(xhr, status, text));
                }
            });
            return df.promise();
        };

        /*
            Показ формы ответа на коммент
        */
        Comments.prototype.replyForm = function($comment) {
            var df = $.Deferred();
            this.removeEmptyForms();
            $comment.find('form').remove();

            var $reply_form = $(this.$reply_form_template);
            $reply_form.find('input[name="parent"]').val($comment.data('id'));
            $comment.append($reply_form);

            $reply_form.find('textarea').keyup().focus();
            return df.resolve($reply_form);
        };

        /*
            Показ формы редактирования комментария
        */
        Comments.prototype.editForm = function($comment) {
            var that = this;
            var df = $.Deferred();
            $.ajax({
                url: window.js_storage.comment_change,
                type: 'GET',
                data: {
                    content_type: that.content_type,
                    object_id: that.object_id,
                    comment: $comment.data('id')
                },
                success: function(response) {
                    if (response.error) {
                        return df.reject(response.error);
                    }
                    that.removeEmptyForms();
                    $comment.find('form').remove();

                    var $edit_form = $(that.$edit_form_template);
                    $comment.append($edit_form);

                    $edit_form.find('textarea').val(response.text).keyup().focus();
                    df.resolve($edit_form);
                },
                error: function(xhr, status, text) {
                    df.reject(that.ajaxError(xhr, status, text));
                }
            });
            return df.promise();
        };

        /*
            Удаление комментария
        */
        Comments.prototype.remove = function($comment) {
            var that = this;
            var df = $.Deferred();
            $.ajax({
                url: window.js_storage.comment_delete,
                type: 'POST',
                data: {
                    content_type: that.content_type,
                    object_id: that.object_id,
                    comment: $comment.data('id')
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
                error: function(xhr, status, text) {
                    df.reject(that.ajaxError(xhr, status, text));
                }
            });
            return df.promise();
        };

        /*
            Удаление комментария
        */
        Comments.prototype.remove = function($comment) {
            var that = this;
            var df = $.Deferred();
            $.ajax({
                url: window.js_storage.comment_delete,
                type: 'POST',
                data: {
                    content_type: that.content_type,
                    object_id: that.object_id,
                    comment: $comment.data('id')
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
                error: function(xhr, status, text) {
                    df.reject(that.ajaxError(xhr, status, text));
                }
            });
            return df.promise();
        };

        /*
            Восстановление комментария
        */
        Comments.prototype.restore = function($comment) {
            var that = this;
            var df = $.Deferred();
            $.ajax({
                url: window.js_storage.comment_restore,
                type: 'POST',
                data: {
                    content_type: that.content_type,
                    object_id: that.object_id,
                    comment: $comment.data('id')
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
                error: function(xhr, status, text) {
                    df.reject(that.ajaxError(xhr, status, text));
                }
            });
            return df.promise();
        };

        /*
            Оценка комментария
        */
        Comments.prototype.vote = function($comment, is_like) {
            var that = this;
            var df = $.Deferred();
            $.ajax({
                url: window.js_storage.comment_vote,
                type: 'POST',
                data: {
                    content_type: that.content_type,
                    object_id: that.object_id,
                    comment: $comment.data('id'),
                    is_like: Number(is_like)
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
                error: function(xhr, status, text) {
                    df.reject(that.ajaxError(xhr, status, text));
                }
            });
            return df.promise();
        };

        /*
            Добавление комментария
        */
        Comments.prototype.post = function($form) {
            var that = this;
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
                        $parent_comment = $form.closest('.' + that.settings.comment_class);

                    if ($parent_comment.length) {
                        // ответ на коммент
                        $form.remove();
                        that.getBranch($parent_comment).last().after($comment);
                    } else {
                        // добавление корневого коммента
                        $wrapper.find('.' + that.settings.comments_container_class).append($comment);
                        $form.find('textarea').val('').keyup();
                    }
                    df.resolve($comment, $parent_comment);
                },
                error: function(xhr, status, text) {
                    df.reject(that.ajaxError(xhr, status, text));
                }
            });
            return df.promise();
        };

        /*
            Редактирование комментария
        */
        Comments.prototype.edit = function($form) {
            var that = this;
            var df = $.Deferred();
            var $comment = $form.closest('.' + that.settings.comment_class);

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
                error: function(xhr, status, text) {
                    df.reject(that.ajaxError(xhr, status, text));
                }
            });
            return df.promise();
        };

        return Comments;
    })();

})(jQuery);