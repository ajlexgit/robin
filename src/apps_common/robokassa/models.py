from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _


class Log(models.Model):
    STATUS_MESSAGE = 1
    STATUS_WARNING = 2
    STATUS_SUCCESS = 3
    STATUS_ERROR = 4
    STATUSES = (
        (STATUS_MESSAGE, _('Message')),
        (STATUS_WARNING, _('Warning')),
        (STATUS_SUCCESS, _('Success')),
        (STATUS_ERROR, _('Error')),
    )

    STEP_RESULT = 1
    STEP_SUCCESS = 2
    STEP_FAIL = 3
    STEPS = (
        (STEP_RESULT, _('Result')),
        (STEP_SUCCESS, _('Success Page')),
        (STEP_FAIL, _('Fail page')),
    )

    inv_id = models.PositiveIntegerField(_('InvId'), blank=True, null=True)
    step = models.PositiveSmallIntegerField(_('step'), choices=STEPS)
    status = models.PositiveSmallIntegerField(_('status'), choices=STATUSES)
    message = models.CharField(_('Message'), max_length=255)
    created = models.DateTimeField(_('create date'), default=now, editable=False)

    class Meta:
        verbose_name = _('log message')
        verbose_name_plural = _('log messages')
        ordering = ('-created', )

    def __str__(self):
        status = dict(self.STATUSES).get(self.status)
        return '[%s] %s' % (status, self.message)

