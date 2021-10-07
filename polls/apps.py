"""Polls config for KU-polls."""

from django.apps import AppConfig


class PollsConfig(AppConfig):
    """Polls config for KU-polls."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'polls'
