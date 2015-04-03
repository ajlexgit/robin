from .models import Comment, CommentVote

"""
    Модуль комментариев.
    Требуется подключить:
        comments/js/comments_class.js
        comments/js/comments.js
    
    Настройки:
        COMMENT_USER_VOTES_CACHE_BACKEND = 'default'
    
    Можно повесить на крон скрипт физического удаления комментариев:
        pm clean_comments
    
    Подключение комментариев к сущности:
        # =====================
        # === template.html ===
        # =====================
        
        {% load comments %}
        ...
        <p class="title-h2"><a href="#comments" name="comments">Комментарии</a></p>
        {% comments post %}
        
        
        # =====================
        # === admin.py ===
        # =====================
        
        from comments.admin import CommentsModelAdminMixin
        
        class PostAdmin(CommentsModelAdminMixin, admin.ModelAdmin):
            suit_comments_position = 'bottom'
            suit_comments_tab = 'main'
            ...
"""