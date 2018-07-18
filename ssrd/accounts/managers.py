from django.db import models


class CredentialManager(models.Manager):
    def add_credential(self, request, user, Type, confirm=False, action=None):
        credential, created = self.get_or_create(
            user=user, Type=Type, defaults={"Type": Type}
        )

        if created and confirm:
            credential.send_confirmation(request, action=action)

        return credential
