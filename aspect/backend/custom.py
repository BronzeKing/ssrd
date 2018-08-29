from django.db.models import Q
from django.conf import settings

from ssrd.users.models import User, AuthorizeCode, Group


class Backend(object):
    """
    Authenticates against settings.AUTH_USER_MODEL.
    """

    def authenticate(self,
                     account: str='',
                     username: str='',
                     password: str='',
                     mobile: str='',
                     **kwargs):
        account = (account and account.lower()) or (
            mobile and mobile.lower()) or (username and username.lower()) or ''
        if settings.DEBUG:
            group = Group.objects.filter(name=account)
            if group:
                return group[0].users.first()
        user = User.objects.filter(Q(username=account) | Q(email=account) | Q(mobile=account)).select_related('profile')
        for u in user:
            if u.check_password(password):
                return u
        ac = AuthorizeCode.objects.filter(
            code=account, status__gt=0).select_related('user')
        if ac:
            return ac[0].user

    def get_user(self, user_id):
        try:
            return User._default_manager.get(pk=user_id)
        except User.DoesNotExist:
            return None
