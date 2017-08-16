from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import parsers, renderers
from django.utils.translation import ugettext as _
from django.contrib.auth import authenticate, get_user_model

from paraer import para_ok_or_400
from . import V, Result


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(label=_("Email"))
    password = serializers.CharField(
        label=_("Password"), style={'input_type': 'password'})

    def validate(self, attrs):
        email = attrs.get('email', '').lower()
        password = attrs.get('password')

        if email and password:
            user = authenticate(email=email, password=password)

            if user:
                # From Django 1.10 onwards the `authenticate` call simply
                # returns `None` for is_active=False users.
                # (Assuming the default `ModelBackend` authentication backend.)
                if not user.is_authenticated():
                    msg = _('User account is disabled.')
                    raise serializers.ValidationError(
                        msg, code='authorization')
            else:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "email " and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class TokenView(APIView):
    permission_classes = ()
    serializer_class = AuthTokenSerializer
    authentication_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser,
                      parsers.JSONParser, )
    renderer_classes = (renderers.JSONRenderer, )
    result_class = Result

    @para_ok_or_400([{
        'name': 'email',
        'method': V.email,
        'description': '用户邮箱'
    }, {
        'name': 'password',
        'description': '用户密码',
        'method': V.password
    }])
    def post(self, request, *args, **kwargs):
        """
        获取用户token
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


class EmailBackend(object):
    """
    Authenticates against settings.AUTH_USER_MODEL.
    """

    def authenticate(self, email=None, username=None, password=None, **kwargs):
        email = email or username or ''
        UserModel = get_user_model()
        user = None
        try:
            user = UserModel.objects.get(email=email.lower())
            if user.check_password(password):
                return user
            else:
                user = None
        except UserModel.DoesNotExist as e:
            user = None

        return user

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel._default_manager.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
