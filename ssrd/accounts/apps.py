from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = "ssrd.accounts"
    verbose_name = "Accounts"

    def ready(self):
        """Override this to put in:
            Users system checks
            Users signal registration
        """
        pass
