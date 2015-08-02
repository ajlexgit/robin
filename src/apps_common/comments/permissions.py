from django.utils.translation import ugettext_lazy as _
from libs.now import now
from . import options
from .voted_cache import get_voted


class CommentException(Exception):
    _reason = ''

    def __init__(self, reason='', *args, **kwargs):
        super().__init__(*args, **kwargs)
        if reason:
            self._reason = reason

    @property
    def reason(self):
        return str(self._reason)

    def __str__(self):
        return self.reason

class UnauthenticatedUser(CommentException):
    _reason = _('Authentication required')


class SelfReplyDenied(CommentException):
    _reason = _('You cannot reply to your own comment')


class SelfVoteDenied(CommentException):
    _reason = _('You cannot vote for your own comment')


class AlreadyVoted(CommentException):
    _reason = _('You have already voted for this comment')


class NoEditPermission(CommentException):
    _reason = _('You don\'t have permission to edit this comment')


class NoDeletePermission(CommentException):
    _reason = _('You don\'t have permission to delete this comment')


class NoRestorePermission(CommentException):
    _reason = _('You don\'t have permission to restore this comment')


class DeletedComment(CommentException):
    _reason = _('This comment was deleted')


class UndeletedComment(CommentException):
    _reason = _('This comment was not deleted')


def check_add(comment, user):
    if not user.is_authenticated():
        raise UnauthenticatedUser


def check_reply(comment, user):
    if not user.is_authenticated():
        raise UnauthenticatedUser

    if not options.ALLOW_REPLY_SELF_COMMENTS and comment.user == user:
        raise SelfReplyDenied


def check_edit(comment, user):
    if not user.is_authenticated():
        raise UnauthenticatedUser

    if comment.deleted:
        raise DeletedComment

    if user.has_perm('comments.change_comment'):
        return

    if options.ALLOW_EDIT_TIME and comment.user == user:
        comment_age = now() - comment.created
        if comment_age.seconds > options.ALLOW_EDIT_TIME:
            raise NoEditPermission
    else:
        raise NoEditPermission


def check_delete(comment, user):
    if not user.is_authenticated():
        raise UnauthenticatedUser

    if comment.deleted:
        raise DeletedComment

    if user.has_perm('comments.delete_comment'):
        return

    if not options.ALLOW_DELETE_SELF_COMMENTS or comment.user != user:
        raise NoDeletePermission


def check_restore(comment, user):
    if not user.is_authenticated():
        raise UnauthenticatedUser

    if not comment.deleted:
        raise UndeletedComment

    if user.has_perm('comments.delete_comment'):
        return

    if not options.ALLOW_DELETE_SELF_COMMENTS or comment.deleted_by != user:
        raise NoRestorePermission


def check_vote(comment, user):
    if not user.is_authenticated():
        raise UnauthenticatedUser

    if not options.ALLOW_VOTE_SELF_COMMENTS and comment.user == user:
        raise SelfVoteDenied

    if comment.deleted:
        raise DeletedComment

    voted = get_voted(user)
    if not voted.get(comment.id) is None:
        raise AlreadyVoted
