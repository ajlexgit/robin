(function($) {

    $(document).ready(function() {
        // Инициализация комментариев
        $('.comments-wrapper').each(function() {
            new Comments(this);
        });

        // Подсвечиваем коммент, если перешли по его якорю
        var current_comment = /comment-(\d+)/.exec(location.hash);
        if (current_comment) {
            var $comment = $('.comment[data-id="'+current_comment[1]+'"]');
            $comment.addClass('comment-highlighted').switchClass('comment-highlighted', '', 2000);
        }
    }).on('formclose.comments', '.comment', function(event, form) {
        $(this).removeClass('inner-form inner-form-reply inner-form-edit');
    }).on('click.comments.reply', '.comment .reply', function() {
        // Форма ответа на коммент
        var $comment = $(this).closest('.comment'),
            object = $comment.closest('.comments-wrapper').data(window.COMMENTS_DATA_NAME);

        object.replyForm($comment).done(function() {
            $comment.addClass('inner-form inner-form-reply');
        });

        return false;
    }).on('click.comments.edit', '.comment .edit', function() {
        // Форма редактирования коммента
        var $comment = $(this).closest('.comment'),
            object = $comment.closest('.comments-wrapper').data(window.COMMENTS_DATA_NAME);

        object.editForm($comment).done(function() {
            $comment.addClass('inner-form inner-form-edit');
        }).fail(function(reason) {
            alert(reason);
        });

        return false;
    }).on('click.comments.delete', '.comment .delete', function() {
        // Удаление коммента
        var $button = $(this),
            $comment = $button.closest('.comment'),
            object = $comment.closest('.comments-wrapper').data(window.COMMENTS_DATA_NAME);
        if ($button.hasClass('disabled')) return false;

        $button.addClass('disabled');
        object.remove($comment).fail(function(reason) {
            alert(reason);
        }).always(function() {
            $button.removeClass('disabled');
        });

        return false;
    }).on('click.comments.restore', '.comment .restore', function() {
        // Восстановление коммента
        var $button = $(this),
            $comment = $button.closest('.comment'),
            object = $comment.closest('.comments-wrapper').data(window.COMMENTS_DATA_NAME);
        if ($button.hasClass('disabled')) return false;

        $button.addClass('disabled');
        object.restore($comment).fail(function(reason) {
            alert(reason);
        }).always(function() {
            $button.removeClass('disabled');
        });

        return false;
    }).on('click.comments.vote', '.comment .rating-like', function() {
        // Голос ЗА коммент
        var $comment = $(this).closest('.comment'),
            $rating = $(this).closest('.rating'),
            object = $comment.closest('.comments-wrapper').data(window.COMMENTS_DATA_NAME);
        if ($rating.hasClass('disabled')) return false;

        $rating.addClass('disabled');
        object.vote($comment, true).fail(function(reason) {
            alert(reason);
            $rating.removeClass('disabled');
        });

        return false;
    }).on('click.comments.vote', '.comment .rating-dislike', function() {
        // Голос ПРОТИВ коммента
        var $comment = $(this).closest('.comment'),
            $rating = $(this).closest('.rating'),
            object = $comment.closest('.comments-wrapper').data(window.COMMENTS_DATA_NAME);
        if ($rating.hasClass('disabled')) return false;

        $rating.addClass('disabled');
        object.vote($comment, false).fail(function(reason) {
            alert(reason);
            $rating.removeClass('disabled');
        });

        return false;
    }).on('click.comments.cancel', '.comment .btn-cancel', function() {
        // Удаление формы при клике на кнопку "Отмена"
        var $comment = $(this).closest('.comment');
        var $form = $(this).closest('form');
        $comment.trigger('formclose', [$form.get(0)]);
        $form.remove();
        return false;
    }).on('submit.comments.post', '.comment-post-form', function() {
        // Добавление комментария
        var $form = $(this),
            object = $form.closest('.comments-wrapper').data(window.COMMENTS_DATA_NAME);
        if ($form.hasClass('disabled')) return false;

        $form.addClass('disabled');
        object.post($form).done(function($comment, $parent_comment) {
            if ($parent_comment.length) {
                // Скролл к новому комментарию
                $.scrollTo($comment, 300, {
                    offset: -Math.round($(window).height() / 2),
                    easing: 'easeOutQuad',
                    onAfter: function() {
                        $comment.addClass('comment-highlighted').switchClass('comment-highlighted', '', 2000);
                    }
                });
            }
        }).fail(function(reason) {
            alert(reason);
        }).always(function() {
            $form.removeClass('disabled');
        });

        return false;
    }).on('submit.comments.change', '.comment-edit-form', function() {
        // Редактирование комментария
        var $form = $(this),
            object = $form.closest('.comments-wrapper').data(window.COMMENTS_DATA_NAME);
        if ($form.hasClass('disabled')) return false;

        $form.addClass('disabled');
        object.edit($form).fail(function(reason) {
            alert(reason);
        }).always(function() {
            $form.removeClass('disabled');
        });

        return false;
    }).on('keyup.comments.textchange change.comments.textchange', '.comments-wrapper textarea', function() {
        // Изменение текста в форме активирует/деактивирует кнопку отправки
        var button = $(this).closest('form').find('.btn-send');
        if ($(this).val()) {
            button.removeClass('disabled').prop('disabled', false);
        } else {
            button.addClass('disabled').prop('disabled', true);
        }
    }).on('login.auth.comments', function() {
        // Обновление комментов при авторизации
        $('.comments-wrapper').each(function() {
            var object = $(this).data(window.COMMENTS_DATA_NAME);
            object.refresh().fail(function(reason) {
                console.error(reason);
            });
        });
    }).on('logout.auth.comments', function() {
        // Обновление комментов при выходе из профиля
        $('.comments-wrapper').each(function() {
            var object = $(this).data(window.COMMENTS_DATA_NAME);
            object.refresh().fail(function(reason) {
                console.error(reason);
            });
        });
    }).on('click.comments', function(event) {
        // TODO: вешать только при открытии формы
        // Удаление пустых форм при клике вне формы комментирования
        $('.comments-wrapper').each(function() {
            if (!$(event.target).closest('form').closest(this).length) {
                var object = $(this).data(window.COMMENTS_DATA_NAME);
                object.removeEmptyForms();
            }
        });
    });

})(jQuery);
