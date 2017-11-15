from django.conf import settings
from django.test import RequestFactory

from ssrd.users.models import User
from ssrd.accounts.models import Credential
from allauth.utils import build_absolute_uri


def main():
    user = User.objects.last()
    request = RequestFactory()
    request.user = user
    response = request.get('/users')
    credential, ok = Credential.objects.get_or_create(user=user, key=0)
    credential.send_confirmation(request, signup=True)

def db():
    print(User.objects.all())
