from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from django.db import models
from django.utils.translation import gettext, gettext_lazy as _
from django.utils import timezone
import logging
logger = logging.getLogger('ilogger')

# Create your models here.
class UserActivity(models.Model):
    action_time = models.DateTimeField(
        _('action time'),
        default=timezone.now,
        editable=False,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.CASCADE,
        related_name="activities",
        verbose_name=_('user'),
    )
    target_ct = models.ForeignKey(
        ContentType,
        models.SET_NULL,
        verbose_name=_('content type'),
        blank=True, null=True,
        related_name="activity_object"
    )
    target_id = models.TextField(_('object id'), blank=True, null=True)

    target = GenericForeignKey('target_ct', 'target_id')

    change_message = models.TextField(_('change message'), blank=True)

    ip_address = models.CharField(_('IP Address'), max_length=20, blank=True, null=True)
    user_agent = models.CharField(_('User agent'), max_length=200, blank=True, null=True)
    path = models.CharField(_('Path'), max_length=256, blank=True, null=True)
    read = models.BooleanField(default=False)

    # ip_Address
    #
    # user_agent request.META['HTTP_USER_AGENT']
    #
    # mac
    #
    # what else?
    #

    class Meta:
        # verbose_name = _('log entry')
        # verbose_name_plural = _('log entries')
        # db_table = 'django_admin_log'
        ordering = ['-action_time']

    def __repr__(self):
        return str(self.action_time)

    def __str__(self):
        return str(self.action_time)
