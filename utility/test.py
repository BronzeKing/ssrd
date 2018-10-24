from allauth.utils import build_absolute_uri
from django.conf import settings
from django.test import RequestFactory

from ssrd.accounts.models import Credential
from ssrd.users.filebrowser import FileBrowser
from ssrd.users.models import Project, User


def main():
    user = User.objects.last()
    request = RequestFactory()
    request.user = user
    response = request.get("/users")
    credential, ok = Credential.objects.get_or_create(user=user, key=0)
    credential.send_confirmation(request, signup=True)


def db():
    print(User.objects.all())


def cache():
    from django.core.cache import cache
    from django.conf import settings

    print(settings.REDIS)
    print(cache.get("asd"))


def profile():
    from ssrd.users.models import Profile, avator

    objs = Profile.objects.all()
    for obj in objs:
        obj.avator = avator
        obj.save()
        print(obj.avator.url)


def sms():
    from ssrd.contrib.utils import SmsClient

    SmsClient.sendCaptcha("14574820226", {"code": "1234"})


def file():
    from ssrd.home.models import Documents
    from django.core.files import File

    with open("cli.py", "rb") as fd:
        file = File(fd)
        doc = Documents.objects.create(name="test111", source=100, file=file)
        import ipdb

        ipdb.set_trace(context=30)
        print(doc)
