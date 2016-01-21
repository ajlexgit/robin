(function($) {

    window.Comments = Class(null, function Comments(cls, superclass) {
        cls.defaults = {
            comment_class: 'comment',
            comments_container_class: 'comments',
            form_container_class: 'comments-form-wrapper',
            reply_template_class: 'comments-reply-template',
            edit_template_class: 'comments-edit-template'
        };

        cls.DATA_KEY = 'comments';


        cls.init = function(root, options) {
            this.$root = $(root).first();
            if (!this.$root.length) {
                return this.raise('root element not found');
            }

            // настройки
            this.opts = $.extend({}, this.defaults, options);

            this.content_type = this.$root.data('content_type');
            this.object_id = this.$root.data('object_id');
            this.$reply_form_template = this.$root.find('.' + this.opts.reply_template_class).html();
            this.$edit_form_template = this.$root.find('.' + this.opts.edit_template_class).html();

            // Удаляем атрибуты, чтобы лишний раз не палить
            this.$root.removeAttr('data-content_type data-object_id');

            this.$root.data(this.DATA_KEY, this);
        };

        // обработка ошибок ajax-запросов
        cls.ajaxError = function(xhr, status, text) {
            if (xhr.responseText) {
                var json_response = $.parseJSON(xhr.responseText);
                if (json_response.message) {
                    return json_response.message;
                }
            }
            return text
        };

        // Возвращает jQuery-коллекцию, содержащий ветку комментариев
        cls.getBranch = function($parent_comment) {
            var that = this;
            var parent_comment_level = $parent_comment.data('level');
            return $parent_comment.nextUntil(function() {
                var $self = $(this);
                return !$self.hasClass(that.opts.comment_class) || $self.data('level') <= parent_comment_level;
            }).addBack();
        };

        // Удаление всех пустых форм
        cls.removeEmptyForms = function() {
            var that = this;
            that.$root.find('.' + that.opts.comments_container_class + ' form').each(function() {
                var $form = $(this);
                var $comment = $form.closest('.' + that.opts.comment_class);
                if (!$form.find('textarea').val()) {
                    $comment.trigger('formclose', [$form.get(0)]);
                    $form.remove();
                }
            });
        };

        // Обновление всего блока комментариев
        cls.refresh = function() {
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
                    that.$root.find('.' + that.opts.comments_container_class).replaceWith(response.comments);
                    that.$root.find('.' + that.opts.form_container_class).replaceWith(response.initial_form);
                    df.resolve();
                },
                error: function(xhr, status, text) {
                    df.reject(that.ajaxError(xhr, status, text));
                }
            });
            return df.promise();
        };

        // Показ формы ответа на коммент
        cls.replyForm = function($comment) {
            var df = $.Deferred();
            this.removeEmptyForms();
            $comment.find('form').each(function() {
                $comment.trigger('formclose', [this]);
                $(this).remove();
            });

            var $reply_form = $(this.$reply_form_template);
            $reply_form.find('input[name="parent"]').val($comment.data('id'));
            $comment.append($reply_form);

            $reply_form.find('textarea').keyup().focus();
            return df.resolve($reply_form);
        };

        // Показ формы редактирования комментария
        cls.editForm = function($comment) {
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
                    that.removeEmptyForms();
                    $comment.find('form').each(function() {
                        $comment.trigger('formclose', [this]);
                        $(this).remove();
                    });

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

        // Удаление комментария
        cls.remove = function($comment) {
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

        // Восстановление комментария
        cls.restore = function($comment) {
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

        // Оценка комментария
        cls.vote = function($comment, is_like) {
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

        // Добавление комментария
        cls.post = function($form) {
            var that = this;
            var df = $.Deferred();
            $.ajax({
                url: window.js_storage.comment_post,
                type: 'POST',
                data: $form.serialize(),
                success: function(response) {
                    var $comment = $(response.html),
                        $parent_comment = $form.closest('.' + that.opts.comment_class);

                    if ($parent_comment.length) {
                        // ответ на коммент
                        that.getBranch($parent_comment).last().after($comment);
                        $parent_comment.trigger('formclose', [$form]);
                        $form.remove();
                    } else {
                        // добавление корневого коммента
                        that.$root.find('.' + that.opts.comments_container_class).append($comment);
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

        // Редактирование комментария
        cls.edit = function($form) {
            var that = this;
            var df = $.Deferred();
            var $comment = $form.closest('.' + that.opts.comment_class);

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
    });

})(jQuery);
