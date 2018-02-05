from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver

from ssrd.users.models import Profile



@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance, name=instance.username)
