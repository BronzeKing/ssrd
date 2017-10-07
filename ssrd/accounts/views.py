from django.contrib import auth
from django.db.models import Q
from rest_framework.authtoken.models import Token
from paraer import para_ok_or_400

from ssrd.contrib.serializer import Serializer
from ssrd.contrib import APIView, V, UnAuthView
from ssrd.users.models import User
from ssrd import const
from .models import Credential, Captcha


class LoginView(UnAuthView):
    @para_ok_or_400([{
        'name': 'account',
        'description': '手机、邮箱或授权码',
        'required': True
    }, {
        'name': 'password',
        'description': '密码'
    }])
    def post(self, request, **kwargs):
        result = self.result_class()
        user = auth.authenticate(**kwargs)
        if not user or not user.is_authenticated:
            return result.error('account', '手机、邮箱、授权码或密码错误')()
        token, created = Token.objects.get_or_create(user=user)
        return result.data(dict(key=token.key))()

    def get(self, request):
        return self.result_class().data(
            dict(status=request.user.is_authenticated()))()


class LogoutView(UnAuthView):
    def post(self, request, **kwargs):
        auth.logout(request)
        return self.result_class().data(dict(status='ok'))()


class RegisterView(UnAuthView):
    serializer_class = Serializer(User)

    @para_ok_or_400([{
        'name': 'name',
        'method': V.name,
        'required': True
    }, {
        'name': 'password',
        'description': '密码',
        'method': V.password,
        'required': True
    }, {
        'name': 'role',
        'description': ('客户类型', ) + const.ROLES,
    }, {
        'name': 'mobile',
        'description': '手机',
        'method': V.mobile,
        'required': True
    }, {
        'name': 'invitation',
        'description': '邀请码',
        'method': V.invitation
    }])
    def post(self,
             request,
             name=None,
             mobile=None,
             password=None,
             role='42',
             invitation=None):
        user = User.objects.create_user(
            name=name, mobile=mobile, password=password, role=role)
        invitation and invitation.users.add(user)
        auth.login(request, user)
        return self.result_class(data=user)(serialize=True)


captchaMap = {"signup": "注册", "resetPassword": "重置密码"}


class CaptchaView(UnAuthView):
    @para_ok_or_400([{
        'name':
        'Type',
        'description': ('类型', ) + tuple(const.CredentialKeyMap.items()),
        'method':
        lambda x: x in const.CredentialKeyMap and x,
        'required':
        True
    }, {
        'name': 'action',
        'description': captchaMap,
        'method': lambda x: x in captchaMap and x
    }])
    def get(self, request, Type=None, action='signup'):
        Captcha.fromUser(request.user, Type).send(request, action)
        return self.result_class().data(dict(status='ok'))()


class CredentialView(APIView):
    serializer_class = Serializer(Credential)

    @para_ok_or_400([{
        'name':
        'Type',
        'description': ('类型', ) + tuple(const.CredentialKeyMap.items()),
        'method':
        lambda x: x in const.CredentialKeyMap and x,
        'required':
        True
    }, {
        'name': 'captcha',
        'description': '验证码'
    }])
    def post(self, request, Type=None, captcha=None):
        result = self.result_class()
        if captcha == Captcha.fromUser(request.user, Type):
            confirm = bool(captcha)
            obj = Credential.objects.add_credential(
                request, request.user, Type, signup=True, confirm=confirm)
            obj.verified = True
            obj.save()
        else:
            return result.error('captcha', '验证码不正确')()

        return result.data(obj)(serialize=True)


class PasswordChangeView(APIView):
    serializer_class = Serializer(User)

    @para_ok_or_400([{
        'name': 'password',
        'method': V.password,
        'description': '密码'
    }, {
        'name': 'password2',
        'method': V.password,
        'description': '再次确认密码'
    }])
    def post(self, request, password=None, password2=None):
        user, result = request.user, self.result_class()
        if password != password2:
            return result.error('password2', '请再次输入相同的值')()
        user.set_password(password2)
        user.save()
        return result.data(user)(serialize=True)


class PasswordResetView(APIView):
    @para_ok_or_400([{
        'name': 'email',
        'method': V.email,
        'description': '用户邮箱'
    }, {
        'name': 'mobile',
        'method': V.moble,
        'description': "手机号码"
    }, {
        'name': 'captcha',
        'description': '验证码'
    }])
    def post(self, request, email=None, mobile=None, captcha=None, **kwargs):
        result = self.result_class()
        if not Captcha.equal(request.user, captcha):
            return result.error('captcha', '验证码不正确')

        user = User.objects.filter(Q(email=email) | Q(mobile=mobile))
        Type = email and 'mobile' or 'email'
        if not user:
            return result.error(Type, "邮箱或者手机号码没有被注册")
        user = user[0]
        credential = Credential.objects.filter(
            user=user, Type=Type, verified=True)
        if not credential:
            return result.error(Type, "邮箱或者手机号码没有被注册")
        credential[0].send_confirmation(request, action='resetPassword')
        return result.data(status='ok')()
