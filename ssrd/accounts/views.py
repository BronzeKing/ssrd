from django.contrib import auth
from django.db.models import Q
from paraer import para_ok_or_400
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework_jwt.settings import api_settings

from ssrd.contrib.serializer import Serializer, UserSerializer
from ssrd.contrib import APIView, V, UnAuthView, Result
from ssrd.users.models import User, Invitation, Profile, Group
from ssrd import const
from .models import Credential, Captcha

from django.http import HttpResponse
import json


def jsonResponse(response):
    response = json.dumps(response)
    return HttpResponse(response, content_type="application/json")


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


def _tokenFromUser(user):
    payload = jwt_payload_handler(user)
    return jwt_encode_handler(payload)


@csrf_exempt
def tokenFromSession(request):
    """
    从session中获取token 用于微信、微博、qq等登录
    """
    token = ""
    if request.user.is_authenticated:
        token = _tokenFromUser(request.user)
        auth.logout(request)
    return jsonResponse(dict(token=token))


class LoginView(APIView):
    authentication_classes = APIView.authentication_classes
    result_class = Result

    @para_ok_or_400(
        [
            {
                "name": "mobile",
                "description": "手机、邮箱或授权码",
                "required": True,
                "msg": "请输入账号",
            },
            {"name": "password", "description": "密码", "msg": "请输入密码"},
        ]
    )
    def post(self, request, **kwargs):
        mobile = kwargs.get("mobile")
        if not mobile:
            return self.result_class().error("mobile", "不能为空")()
        user = auth.authenticate(**kwargs)
        if not user:
            return self.result_class().error("mobile", "手机、邮箱、授权码或密码错误")(status=400)
        token = _tokenFromUser(user)
        return self.result_class().data(dict(token=token))()

    def get(self, request):

        user = request.user
        if not user.is_authenticated:
            return self.result_class(data=dict(url="login"))()
        data = UserSerializer(user).data
        profile = Serializer(Profile)(user.profile).data
        verified = {"email": False, "mobile": False}
        verified.update({x.Type: x.verified for x in user.credentials.all()})
        data.update(profile=profile, verified=verified, invitation=user.profile.code)
        return self.result_class(data=data)(serialize=True)


class LogoutView(UnAuthView):
    def post(self, request, **kwargs):
        auth.logout(request)
        return self.result_class().data(dict(status="ok"))()

    def get(self, request, **kwargs):
        auth.logout(request)
        return self.result_class().data(dict(status="ok"))()


class RegisterView(UnAuthView):
    serializer_class = Serializer(User, extra=["profile"])

    @para_ok_or_400(
        [
            {"name": "username", "method": V.name, "required": True},
            {
                "name": "password",
                "description": "密码",
                "method": V.password,
                "required": True,
            },
            {"name": "group", "description": "用户组"},
            {"name": "role", "description": "客户角色", **V.make(const.ROLES)},
            {
                "name": "mobile",
                "description": "手机",
                "method": V.mobile,
                "required": True,
            },
            {"name": "email", "description": "邮箱", "method": V.email},
            {"name": "invitation", "description": "邀请码", "method": V.invitation},
        ]
    )
    def post(
        self,
        request,
        username=None,
        mobile=None,
        email="",
        password=None,
        group=None,
        role=None,
        invitation=None,
    ):
        result = self.result_class()
        if email and User.objects.filter(email=email):
            return result.error("email", "该邮箱已被注册")()
        if mobile and User.objects.filter(mobile=mobile):
            return result.error("mobile", "该手机已被注册")()
        group, ok = Group.objects.get_or_create(name=group)
        data = dict(
            username=username, mobile=mobile, email=email, group=group, role=role
        )
        user = User(**data)
        user.set_password(password)
        user.save()
        if invitation:
            Invitation.objects.create(creator=invitation, user=user)
        return result.data(user)(serialize=True)


captchaMap = {
    "register": "注册",
    "resetPassword": "重置密码",
    "changeEmail": "更改邮箱",
    "changeMobile": "更改手机",
}


class CaptchaView(UnAuthView):
    @para_ok_or_400(
        [
            {
                "name": "action",
                "description": captchaMap,
                "method": lambda x: x in captchaMap and x,
                "required": True,
            },
            {"name": "mobile", "description": "手机号码", "method": V.mobile},
            {"name": "email", "description": "邮箱", "method": V.email},
        ]
    )
    def get(self, request, email=None, mobile="", action="register"):
        if not email and not mobile:
            return self.result_class().error("mobile", "不能为空").error("email", "不能为空")()
        if not request.user.is_authenticated:
            request.user.email = email
            request.user.mobile = mobile
        Type = email and "email" or "mobile"
        Captcha.fromUser(request.user, Type).send(request, action)
        return self.result_class().data(dict(status="ok"))()


class CredentialView(APIView):
    serializer_class = Serializer(Credential)

    @para_ok_or_400(
        [
            {"name": "email", "description": "邮箱", "method": V.email},
            {"name": "mobile", "description": "手机", "method": V.mobile},
            {"name": "captcha", "description": "验证码"},
        ]
    )
    def post(self, request, email=None, mobile=None, captcha=None):
        result = self.result_class()
        if not mobile and not email:
            result.error("mobile", "请填写手机号码")
            result.error("email", "请填写邮箱")
            return result()
        Type = mobile and "mobile" or "email"
        if captcha == Captcha.fromUser(request.user, Type, action="destroy"):
            obj = Credential.objects.add_credential(
                request, request.user, Type, action=True, confirm=False
            )
            obj.verified = True
            obj.save()
            setattr(request.user, Type, mobile or email)
            request.user.save()
        else:
            return result.error("captcha", "验证码不正确")()

        return result.data(obj)(serialize=True)


class PasswordChangeView(APIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    @para_ok_or_400(
        [
            {"name": "password", "method": V.password, "description": "密码"},
            {"name": "password2", "method": V.password, "description": "再次确认密码"},
        ]
    )
    def post(self, request, password=None, password2=None):
        user, result = request.user, self.result_class()
        if password != password2:
            return result.error("password2", "请再次输入相同的值")()
        user.set_password(password2)
        user.save()
        return result.data(user)(serialize=True)


class PasswordResetView(APIView):
    permission_classes = (IsAuthenticated,)

    @para_ok_or_400(
        [
            {"name": "email", "method": V.email, "description": "用户邮箱"},
            {"name": "mobile", "method": V.moble, "description": "手机号码"},
            {"name": "captcha", "description": "验证码"},
        ]
    )
    def post(self, request, email=None, mobile=None, captcha=None, **kwargs):
        result = self.result_class()
        if not Captcha.equal(request.user, captcha):
            return result.error("captcha", "验证码不正确")

        user = User.objects.filter(Q(email=email) | Q(mobile=mobile))
        Type = email and "mobile" or "email"
        if not user:
            return result.error(Type, "邮箱或者手机号码没有被注册")
        user = user[0]
        credential = Credential.objects.filter(user=user, Type=Type, verified=True)
        if not credential:
            return result.error(Type, "邮箱或者手机号码没有被注册")
        credential[0].send_confirmation(request, action="resetPassword")
        return result.data(status="ok")()
