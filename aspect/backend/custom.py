from django.db.models import Q

from ssrd.users.models import User, AuthorizeCode


class Backend(object):
    """
    Authenticates against settings.AUTH_USER_MODEL.
    """

    def authenticate(self,
                     account='',
                     username='',
                     password=None,
                     mobile='',
                     **kwargs):
        account = (account and account.lower()) or (
            mobile and mobile.lower()) or (username and username.lower()) or ''
        user = User.objects.filter(Q(email=account) | Q(mobile=account))
        if user:
            user = user[0]
            if user.check_password(password):
                return user
        ac = AuthorizeCode.objects.filter(
            code=account, status__gt=0).select_related('user')
        if ac:
            return ac[0].user

    def get_user(self, user_id):
        try:
            return User._default_manager.get(pk=user_id)
        except User.DoesNotExist:
            return None
