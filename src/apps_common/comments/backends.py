from django.contrib.auth.backends import ModelBackend
from libs.now import now
from . import options
from .models import Comment
from .voted_cache import get_voted


class CommentPermissionsBackend(ModelBackend):
    def get_all_permissions(self, user_obj, obj=None):
        if user_obj.is_anonymous():
            return set()

        result = {'comments.can_post'}

        if isinstance(obj, Comment):
            # can reply
            if obj.user != user_obj or options.ALLOW_REPLY_SELF_COMMENTS:
                result.add('comments.can_reply')


            if obj.deleted:
                # can restore
                if user_obj.has_perm('comments.delete_comment'):
                    result.add('comments.can_restore')
                elif obj.deleted_by == user_obj and options.ALLOW_DELETE_SELF_COMMENTS:
                    result.add('comments.can_restore')
            else:
                # can edit
                if user_obj.has_perm('comments.change_comment'):
                    result.add('comments.can_edit')
                elif options.ALLOW_EDIT_TIME and obj.user == user_obj:
                    comment_age = now() - obj.created
                    if comment_age.seconds <= options.ALLOW_EDIT_TIME:
                        result.add('comments.can_edit')

                # can delete
                if user_obj.has_perm('comments.delete_comment'):
                    result.add('comments.can_delete')
                elif obj.user == user_obj and options.ALLOW_DELETE_SELF_COMMENTS:
                    result.add('comments.can_delete')

                # can vote
                if obj.user != user_obj or options.ALLOW_VOTE_SELF_COMMENTS:
                    voted = get_voted(user_obj)
                    if voted.get(obj.id) is None:
                        result.add('comments.can_vote')
        else:
            pass

        return result
