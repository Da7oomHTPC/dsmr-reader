from datetime import time

from django.db import models
from django.utils.translation import ugettext_lazy as _
from solo.models import SingletonModel


class BackupSettings(SingletonModel):
    """ Generic backup settings. """
    daily_backup = models.BooleanField(
        default=True,
        verbose_name=_('Backup daily'),
        help_text=_('Create a backup of your data daily. Stored locally, but can be exported using Dropbox.')
    )
    compress = models.BooleanField(
        default=True,
        verbose_name=_('Compress'),
        help_text=_('Create backups in compressed (gzip) format, saving a significant amount of disk space.')
    )
    backup_time = models.TimeField(
        default=time(hour=2),
        verbose_name=_('Backup timestamp'),
        help_text=_(
            'Daily moment of creating the backup. You should prefer a nightly timestamp, as it '
            'might freeze or lock the application shortly during backup creation.'
        )
    )
    latest_backup = models.DateTimeField(
        default=None,
        null=True,
        blank=True,
        verbose_name=_('Latest backup'),
        help_text=_(
            'Timestamp of latest backup created. Automatically updated by application. Please note '
            'that the application will ignore the "backup_time" setting the first time used.'
        )
    )

    def __str__(self):
        return self._meta.verbose_name.title()

    class Meta:
        default_permissions = tuple()
        verbose_name = _('Backup configuration')


class DropboxSettings(SingletonModel):
    """ Dropbox backup upload settings. """
    access_token = models.CharField(
        max_length=128,
        default=None,
        null=True,
        blank=True,
        verbose_name=_('Dropbox access token'),
    )
    latest_sync = models.DateTimeField(
        default=None,
        null=True,
        blank=True,
        verbose_name=_('Latest sync'),
        help_text=_('Timestamp of latest sync with Dropbox. Automatically updated by application.')
    )
    next_sync = models.DateTimeField(
        default=None,
        null=True,
        blank=True,
        verbose_name=_('Next sync'),
        help_text=_('Timestamp of next sync with Dropbox. Automatically updated by application.')
    )

    def __str__(self):
        return self._meta.verbose_name.title()

    class Meta:
        default_permissions = tuple()
        verbose_name = _('Dropbox configuration')


class EmailBackupSettings(SingletonModel):
    """ Backup by email settings. """
    INTERVAL_DAILY = 1
    INTERVAL_WEEKLY = 7
    INTERVAL_BIWEEKLY = 14
    INTERVAL_MONTHLY = 28

    INTERVAL_CHOICES = (
        (INTERVAL_DAILY, _('Daily')),
        (INTERVAL_WEEKLY, _('Weekly')),
        (INTERVAL_BIWEEKLY, _('Every two weeks')),
        (INTERVAL_MONTHLY, _('Every four weeks')),
    )

    email_to = models.EmailField(
        max_length=255,
        default=None,
        null=True,
        blank=True,
        help_text=_('The email address to send the backup to')
    )
    interval = models.IntegerField(
        default=INTERVAL_DAILY,
        choices=INTERVAL_CHOICES,
        help_text=_('The frequency of sending backups per email')
    )
    latest_sync = models.DateTimeField(
        default=None,
        null=True,
        blank=True,
        verbose_name=_('Latest sync'),
        help_text=_('Timestamp of latest email sent successfully. Automatically updated by application')
    )
    next_sync = models.DateTimeField(
        default=None,
        null=True,
        blank=True,
        verbose_name=_('Next sync'),
        help_text=_('Timestamp of next email sent. Automatically updated by application')
    )

    def __str__(self):
        return self._meta.verbose_name.title()

    class Meta:
        default_permissions = tuple()
        verbose_name = _('Email backup configuration')
