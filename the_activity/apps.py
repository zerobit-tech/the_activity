from django.apps import AppConfig


class TheActivityConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'the_activity'
    def ready(self):
        # import the_users.signals
        # import the_activity.agents
        from . import signals

        from . import signals_handlers