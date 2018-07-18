from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver

from ssrd.users.models import Profile, Project, Directory


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance, name=instance.username)


@receiver(post_save, sender=Project)
def createDirectory(sender, instance=None, created=False, **kwargs):
    """
    新建项目的文档目录
    """
    if created:
        _createDirectory(instance)


def _createDirectory(project):
    names = ["签证", "设计方案", "合同"]
    Directory.objects.bulk_create([Directory(project=project, name=x) for x in (names)])
