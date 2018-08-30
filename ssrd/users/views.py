import os

import requests
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files import File
from django.db.models import Q
from django.views.generic import RedirectView
from paraer import para_ok_or_400, perm_ok_or_403
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings

from ssrd import const
from ssrd.contrib import APIView, UnAuthView, V, ViewSet
from ssrd.contrib.serializer import ProjectSerializer, Serializer, UserSerializer
from ssrd.users import models as m
from ssrd.users.steps import Step

from .filebrowser import FileBrowser
from .models import (
    AuthorizeCode,
    Collected,
    Documents,
    Invitation,
    Message,
    Profile,
    Project,
    ProjectGroup,
    ProjectLog,
    User,
)

jwt_decode_handler = api_settings.JWT_DECODE_HANDLER


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return "http://{}/#/login?do=token".format(settings.FE_DOMAIN)


class MediaRedirectView(RedirectView):
    permanent = False

    def get_redirect_url(self):
        return const.MediaUrl

    def dispatch(self, request, *args, **kwargs):
        response = super(MediaRedirectView, self).dispatch(request, *args, **kwargs)
        projectId, token = request.GET["projectId"], request.GET["token"].split(" ")[-1]
        userId = jwt_decode_handler(token)["user_id"]
        project = Project.objects.get(id=projectId)
        token = FileBrowser.auth(project=project)
        if "Forbidden" in token:
            FileBrowser.createUser(project)
            token = FileBrowser.auth(project=project)
        response.set_cookie(
            "auth", token, domain="." + const.MediaDomain.split(".", 1)[-1]
        )
        return response


@para_ok_or_400(
    [
        {
            "name": "role",
            "method": V.role,
            "description": ("用户角色, 默认为4，即常规用户",) + const.ROLES,
        },
        {"name": "email", "method": V.email, "required": True, "description": "用户邮箱"},
        {
            "name": "password",
            "method": V.password,
            "required": True,
            "description": "用户密码",
        },
        {"name": "username", "method": V.name, "required": True, "description": "用户名"},
    ]
)
def post(self, request, username=None, role=4, email=None, password=None, **kwargs):
    result = self.result_class()
    if role < getattr(request.user, "role", -10):  # 可以为匿名用户
        return result(403)
    data = dict()
    username and data.update(username=username)
    email and data.update(email=email)
    role and data.update(role=role)
    user = User(**data)
    password and user.set_password(password)
    user.save()
    return result.data(user)(serialize=True)


class UserView(UnAuthView):
    serializer_class = UserSerializer

    post = post
    post.__doc__ = "新建用户"


class UserViewSet(ViewSet):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    @para_ok_or_400(
        [
            {"name": "role", **V.enum(const.ROLES)},
            {"name": "status", **V.enum(const.STATUS)},
            {"name": "search", "description": "按名称搜索"},
            {"name": "group", "method": V.group, "description": "按部门搜索"},
        ]
    )
    def list(self, request, role=None, group=None, search=None, status=None, **kwargs):
        """"""
        query = dict()
        role and query.update(role=role)
        status and query.update(status=status)
        group and query.update(group=group)
        obj = User.objects.filter(**query).exclude(id=request.user.id).order_by("-id")
        if search:
            obj = obj.filter(
                Q(username__contains=search)
                | Q(email__contains=search)
                | Q(mobile__contains=search)
            )
        return self.result_class(data=obj)(serialize=True)

    create = post

    @para_ok_or_400(
        [
            {"name": "pk", "method": V.user, "description": "用户ID", "replace": "user"},
            {"name": "group", "method": V.group, "description": "用户组ID"},
            {"name": "username", "method": V.name, "description": "用户名称"},
            {"name": "email", "method": V.email, "description": "用户邮箱"},
            {
                "name": "status",
                "method": V.Status,
                "description": ("用户状态过滤",) + const.STATUS,
            },
        ]
    )
    @perm_ok_or_403(
        [{"method": lambda r, k: r.user.has_permission(k["user"]), "reason": "无权限"}]
    )
    def update(self, request, user=None, **kwargs):
        """更新用户"""
        [setattr(user, k, v) for k, v in kwargs.items() if v]
        user.save()
        return self.result_class(user)(serialize=True)

    @para_ok_or_400(
        [{"name": "pk", "method": V.user, "description": "用户ID", "replace": "user"}]
    )
    @perm_ok_or_403(
        [{"method": lambda r, k: r.user.has_permission(k["user"]), "reason": "无权限"}]
    )
    def destroy(self, request, user, **kwargs):
        """
        删除用户
        """
        user.delete()
        return self.result_class().data(user)(serialize=True)

    @para_ok_or_400(
        [{"name": "pk", "method": V.user, "description": "用户ID", "replace": "user"}]
    )
    @perm_ok_or_403(
        [{"method": lambda r, k: r.user.has_permission(k["user"]), "reason": "无权限"}]
    )
    def retrieve(self, request, user, **kwargs):
        """
        获取用户
        """
        return self.result_class().data(user)(serialize=True)


class ProfileView(APIView):
    serializer_class = Serializer(Profile)
    permission_classes = (IsAuthenticated,)

    @para_ok_or_400([{"name": "user", "method": V.user, "description": "用户ID"}])
    def get(self, request, user=None, **kwargs):
        return self.result_class().data(user.profile)(serialize=True)

    @para_ok_or_400(
        [
            {
                "name": "userId",
                "method": V.user,
                "replace": "user",
                "description": "用户ID",
            },
            {"name": "gender", "method": V.gender, "description": "性别"},
            {"name": "name", "description": "真实姓名", "method": V.name},
            {"name": "birthday", "description": "生日", "method": V.date},
            {"name": "company", "description": "所属公司", "method": V.name},
            {"name": "position", "description": "职位", "method": V.name},
            {"name": "qq", "description": "QQ号码", "method": V.num},
            {"name": "address", "description": "地址", "method": V.name},
        ]
    )
    def post(self, request, userId=None, user=None, **kwargs):
        profile = request.user.profile
        [setattr(profile, k, v) for k, v in kwargs.items() if v]
        profile.save()
        return self.result_class(data=profile)(serialize=True)


class AuthorizeCodeViewSet(ViewSet):
    serializer_class = Serializer(AuthorizeCode, extra=["user"])
    permission_classes = (IsAuthenticated,)

    @para_ok_or_400(
        [
            {"name": "user", "method": V.user, "description": "用户ID"},
            {"name": "search", "description": "名称搜索过滤"},
            {
                "name": "status",
                "method": V.Status,
                "description": ("状态过滤",) + const.STATUS,
            },
        ]
    )
    def list(self, request, user=None, status=None, search=None, **kwargs):
        query = dict()
        request.user.role > 0 and query.update(creator=request.user)
        status and query.update(status=status)
        obj = AuthorizeCode.objects.filter(**query)
        if search:
            obj = obj.filter(Q(user__username__contains=search))
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400([{"name": "name", "method": V.name, "description": "授权码名称"}])
    def create(self, request, name, **kwargs):
        """新建授权码"""
        if AuthorizeCode.objects.filter(name=name, creator=request.user):
            return self.result_class().error("name", "已存在同名的授权码")()
        obj = AuthorizeCode(name=name, creator=request.user).generateUser()
        obj.save()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400(
        [
            {
                "name": "pk",
                "method": V.authorizecode,
                "description": "授权码ID",
                "replace": "obj",
            },
            {
                "name": "status",
                "method": V.num,
                "description": ("授权码状态过滤",) + const.STATUS,
            },
        ]
    )
    @perm_ok_or_403(
        [
            {
                "method": lambda r, k: r.user.has_permission(k["obj"]),
                "reason": "无权限更改此授权码",
            }
        ]
    )
    def update(self, request, obj=None, status=None, **kwargs):
        """更新授权码"""
        obj.status = status
        obj.save()
        return self.result_class(obj)(serialize=True)

    @para_ok_or_400(
        [
            {
                "name": "pk",
                "method": V.authorizecode,
                "description": "授权码ID",
                "replace": "obj",
            }
        ]
    )
    @perm_ok_or_403(
        [
            {
                "method": lambda r, k: r.user.has_permission(k["obj"]),
                "reason": "无权限更改此授权码",
            }
        ]
    )
    def destroy(self, request, obj=None, status=None, **kwargs):
        """删除授权码"""
        obj.delete()
        return self.result_class(obj)(serialize=True)

    @para_ok_or_400(
        [
            {
                "name": "pk",
                "method": V.authorizecode,
                "description": "授权码ID",
                "replace": "obj",
            }
        ]
    )
    @perm_ok_or_403(
        [
            {
                "method": lambda r, k: r.user.has_permission(k["obj"]),
                "reason": "无权限更改此授权码",
            }
        ]
    )
    def retrieve(self, request, obj=None, **kwargs):
        """获取单个授权码"""
        return self.result_class(obj)(serialize=True)


class InvitationViewSet(ViewSet):
    serializer_class = Serializer(Invitation)

    @para_ok_or_400([{"name": "user", "method": V.user, "description": "所属用户过滤"}])
    def list(self, request, user=None, **kwargs):
        """
        获取受登录用户邀请的用户列表
        """
        query = dict()
        request.user.role == 0 and user and query.update(creator=request.user)
        its = Invitation.objects.filter(**query)
        return self.result_class(data=its)(serialize=True)


class ProjectViewSet(ViewSet):
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated,)

    @para_ok_or_400(
        [
            {"name": "status", **V.enum(const.ProjectStatus)},
            {"name": "group", "method": V.projectGroup, "description": "项目组ID"},
            {"name": "search", "description": "名称搜索过滤"},
        ]
    )
    def list(self, request, status=None, group=None, search=None, **kwargs):
        """
        获取受登录用户有权限的项目
        内部员工获取全量的 && 处于有权限的状态的项目
        外部员工获取全量的有权限的项目
        """

        user = request.user
        query = dict()
        user.group.isCustom() and user.role > 0 and query.update(user=user)  # 内部员工获取全量项目
        status = [x.step for x in Step.steps(user)]
        if "status" in kwargs:
            status = set(status + kwargs["status"])
        status and query.update(status__in=status)
        group and query.update(group=group)
        obj = (
            Project.objects.filter(**query)
            .select_related("user")
            .prefetch_related("attatchment")
            .order_by("-updated")
        )
        if search:
            obj = obj.filter(name__contains=search)
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400(
        [
            {"name": "name", "description": "项目名称", "method": V.name, "required": True},
            {
                "name": "attatchment",
                "description": "项目文档",
                "method": V.documents,
                "type": "file",
            },
            {"name": "type", "required": True, **V.make(const.ProjectType)},
            {
                "name": "mobile",
                "description": "手机",
                "method": V.mobile,
                "required": True,
            },
            {"name": "linkman", "description": "联系人", "required": True},
            {"name": "address", "description": "项目地址"},
            {"name": "remark", "description": "补充说明"},
            {"name": "content", "method": V.json, "description": "项目内容"},
            {"name": "budget", "method": V.num, "required": True, "description": "预算"},
            {"name": "group", "method": V.name, "description": "项目组"},
            {
                "name": "duration",
                "method": V.num,
                "required": True,
                "description": "工期",
            },
        ]
    )
    def create(self, request, group=None, attatchment=None, **kwargs):
        """新建项目"""
        group, ok = ProjectGroup.objects.get_or_create(
            user=request.user, name=group or kwargs["name"]
        )
        not kwargs["content"] and kwargs.update(content=[])
        obj, ok = Project.objects.get_or_create(
            user=request.user, group=group, **kwargs
        )
        attatchment and obj.attatchment.add(*attatchment)
        FileBrowser.createUser(obj)
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400(
        [
            {
                "name": "pk",
                "method": V.project,
                "description": "项目ID",
                "replace": "obj",
            },
            {"name": "status", **V.enum(const.ProjectStatus)},
            {"name": "name", "description": "项目名称", "method": V.name, "required": True},
            {
                "name": "attatchment",
                "description": "项目文档",
                "method": V.files,
                "type": "file",
            },
            {
                "name": "type",
                "description": ("项目类型",) + const.ProjectType,
                "method": lambda x: x in dict(const.ProjectType) and x,
            },
            {
                "name": "mobile",
                "description": "手机",
                "method": V.mobile,
                "required": True,
            },
            {"name": "linkman", "description": "联系人", "required": True},
            {"name": "address", "description": "项目地址"},
            {"name": "remark", "description": "补充说明"},
            {"name": "content", "method": V.json, "description": "项目内容"},
            {"name": "budget", "method": V.num, "description": "预算"},
            {"name": "group", "method": V.name, "description": "项目组"},
            {"name": "duration", "method": V.num, "description": "工期"},
        ]
    )
    @perm_ok_or_403(
        [{"method": lambda r, k: r.user.has_permission(k["obj"]), "reason": "无权限更改此项目"}]
    )
    def update(self, request, obj=None, group=None, name=None, status=None, **kwargs):
        """更新项目"""
        group, ok = ProjectGroup.objects.get_or_create(
            name=group or name, user=obj.user
        )
        status and setattr(obj, "status", status)
        name and setattr(obj, "name", name)
        group and setattr(obj, "group", group)
        obj.save()
        return self.result_class(obj)(serialize=True)

    @para_ok_or_400(
        [{"name": "pk", "method": V.project, "description": "项目ID", "replace": "obj"}]
    )
    @perm_ok_or_403(
        [{"method": lambda r, k: r.user.has_permission(k["obj"]), "reason": "无权限删除此项目"}]
    )
    def destroy(self, request, obj=None, status=None, **kwargs):
        """删除项目"""
        obj.delete()
        return self.result_class(obj)(serialize=True)

    @para_ok_or_400(
        [{"name": "pk", "method": V.project, "description": "项目ID", "replace": "obj"}]
    )
    @perm_ok_or_403(
        [{"method": lambda r, k: r.user.has_permission(k["obj"]), "reason": "无权限查看此项目"}]
    )
    def retrieve(self, request, obj=None, **kwargs):
        """获取单个项目"""
        return self.result_class(obj)(serialize=True)


class ProjectLogViewSet(ViewSet):
    serializer_class = Serializer(ProjectLog, dep=2)
    permission_classes = (IsAuthenticated,)

    @para_ok_or_400(
        [
            {
                "name": "projectId",
                "method": V.project,
                "description": "项目ID",
                "replace": "project",
            },
            {"name": "action", **V.make(const.ProjectLog)},
        ]
    )
    def list(self, request, project=None, action=None, **kwargs):
        """
        获取项目日志，如签证，工作日志，审核日志等
        """
        query = dict()
        project and query.update(project=project)
        action and query.update(action=action)
        obj = ProjectLog.objects.filter(**query).order_by("-updated")
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400(
        [
            {
                "name": "projectId",
                "method": V.project,
                "description": "项目ID",
                "replace": "project",
            },
            {"name": "action", "required": True, **V.make(const.ProjectLog)},
            {"name": "content", "description": "内容"},
            {
                "name": "attatchment",
                "method": V.documents,
                "description": "附件，可以传list",
                "type": "file",
            },
            {"name": "date", "method": V.date, "description": "工作时间"},
        ]
    )
    def create(self, request, project=None, action=None, attatchment=None, **kwargs):
        """
        新建项目日志
        content: {date: '', content: ''}
        """
        obj = ProjectLog.objects.create(project=project, action=action, content=kwargs)
        obj.attatchment.add(*(attatchment or []))
        project.status = Step(project.status)(request.user, action, project=project).step
        project.save()
        return self.result_class(data=obj)(serialize=True)


class CollectViewSet(ViewSet):
    serializer_class = Serializer(Collected, dep=1)
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        """
        获取登录用户的收藏列表
        """
        query = dict()
        request.user.role > 0 and query.update(user=request.user)
        objs = Collected.objects.filter(**query)
        return self.result_class(objs)(serialize=True)

    @para_ok_or_400(
        [
            {
                "name": "productId",
                "method": V.product,
                "description": "产品ID",
                "replace": "obj",
                "required": True,
            }
        ]
    )
    def create(self, request, obj=None, **kwargs):
        """
        新建收藏
        """
        if not request.user.is_authenticated:
            request.user = User.objects.first()
        obj, ok = Collected.objects.get_or_create(user=request.user, product=obj)
        return self.result_class(obj)(serialize=True)

    @para_ok_or_400(
        [{"name": "pk", "method": V.collect, "description": "收藏品ID", "replace": "obj"}]
    )
    @perm_ok_or_403(
        [{"method": lambda r, k: r.user.has_permission(k["obj"]), "reason": "无权限删除此收藏"}]
    )
    def destroy(self, request, obj=None, **kwargs):
        """
        删除收藏
        """
        obj.delete()
        return self.result_class(obj)(serialize=True)

    @para_ok_or_400(
        [{"name": "pk", "method": V.collect, "description": "收藏品ID", "replace": "obj"}]
    )
    @perm_ok_or_403(
        [{"method": lambda r, k: r.user.has_permission(k["obj"]), "reason": "无权限删除此收藏"}]
    )
    def retrieve(self, request, obj=None, **kwargs):
        """
        删除收藏
        """
        return self.result_class(obj)(serialize=True)


class MessageViewSet(ViewSet):
    serializer_class = Serializer(Message, dep=0)

    @para_ok_or_400([{"name": "read", "description": ("已读",) + const.READ}])
    def list(self, request, read=None, **kwargs):
        """
        获取登录用户的消息列表
        """
        query = dict(userId=request.user.id)
        read and query.update(read=read)
        objs = Message.objects.filter(**query).order_by("rank", "-created")
        return self.result_class(objs)(serialize=True)

    @para_ok_or_400(
        [
            {"name": "userId", "description": "所属用户ID", "method": V.user},
            {"name": "title", "description": "标题", "required": True},
            {"name": "content", "description": "内容", "required": True},
        ]
    )
    def create(self, request, title=None, user=None, content=None, **kwargs):
        """
        新建消息
        """
        user = user or request.user
        obj = Message.objects.create(userId=user.id, title=title, content=content)
        #  obj = Message.objects.bulk_create(
        #  (Message(userId=x, title=title, content=content)
        #  for x in User.objects.filter(role__gt=10)))
        return self.result_class(obj)(serialize=True)

    @para_ok_or_400(
        [
            {
                "name": "pk",
                "method": V.message,
                "description": "消息ID",
                "replace": "obj",
            },
            {"name": "title", "description": "消息标题"},
            {"name": "content", "description": "消息内容"},
            {"name": "read", "description": "已读"},
        ]
    )
    @perm_ok_or_403(
        [{"method": lambda r, k: r.user.has_permission(k["obj"]), "reason": "无权限修改此消息"}]
    )
    def update(self, request, obj=None, **kwargs):
        """
        修改消息
        """
        [setattr(obj, k, v) for k, v in kwargs.items() if v]
        obj.save()
        return self.result_class(obj)(serialize=True)

    @para_ok_or_400(
        [{"name": "pk", "method": V.message, "description": "消息ID", "replace": "obj"}]
    )
    @perm_ok_or_403(
        [{"method": lambda r, k: r.user.has_permission(k["obj"]), "reason": "无权限删除此消息"}]
    )
    def destroy(self, request, obj=None, **kwargs):
        """
        删除消息
        """
        obj.delete()
        return self.result_class(obj)(serialize=True)

    @para_ok_or_400(
        [{"name": "pk", "method": V.message, "description": "消息ID", "replace": "obj"}]
    )
    @perm_ok_or_403(
        [{"method": lambda r, k: r.user.has_permission(k["obj"]), "reason": "无权限删除此消息"}]
    )
    def retrieve(self, request, obj=None, **kwargs):
        """
        获取消息
        """
        return self.result_class(obj)(serialize=True)


class GroupViewSet(ViewSet):
    serializer_class = Serializer(m.Group, dep=0)
    permission_classes = (IsAuthenticated,)

    @para_ok_or_400([{"name": "search", "description": "部门搜索"}])
    def list(self, request, search="", **kwargs):
        """
        获取所有部门
        """
        query = dict()
        search and query.update(name__contains=search)
        objs = m.Group.objects.filter(**query)
        return self.result_class(objs)(serialize=True)

    @para_ok_or_400(
        [{"name": "name", "method": V.name, "description": "部门名称", "required": True}]
    )
    def create(self, request, **kwargs):
        """
        新建部门
        """
        obj, ok = m.Group.objects.get_or_create(**kwargs)
        return self.result_class(obj)(serialize=True)

    @para_ok_or_400(
        [
            {"name": "id", "method": V.group, "description": "部门ID", "replace": "obj"},
            {"name": "name", "method": V.name, "description": "部门名称", "required": True},
        ]
    )
    @perm_ok_or_403(
        [{"method": lambda r, k: r.user.has_permission(k["obj"]), "reason": "无权限删除此部门"}]
    )
    def update(self, request, obj=None, **kwargs):
        """
        编辑部门
        """
        [setattr(obj, k, v) for k, v in kwargs.items() if v]
        obj.save()
        return self.result_class(obj)(serialize=True)

    @para_ok_or_400(
        [{"name": "pk", "method": V.group, "description": "部门ID", "replace": "obj"}]
    )
    @perm_ok_or_403(
        [{"method": lambda r, k: r.user.has_permission(k["obj"]), "reason": "无权限删除此部门"}]
    )
    def destroy(self, request, obj=None, **kwargs):
        """
        删除部门
        """
        obj.delete()
        return self.result_class(obj)(serialize=True)

    @para_ok_or_400(
        [{"name": "pk", "method": V.group, "description": "部门ID", "replace": "obj"}]
    )
    @perm_ok_or_403(
        [{"method": lambda r, k: r.user.has_permission(k["obj"]), "reason": "无权限删除此部门"}]
    )
    def retrieve(self, request, obj=None, **kwargs):
        """
        删除部门
        """
        return self.result_class(obj)(serialize=True)


class CartView(APIView):
    serializer_class = Serializer(m.Cart, dep=0)
    permission_classes = (IsAuthenticated,)

    @para_ok_or_400([{"name": "content", "description": "购物车内容", "required": True}])
    def post(self, request, content=None, **kwargs):
        """
        编辑购物车
        """
        obj, ok = m.Cart.objects.get_or_create(user=request.user)
        if not isinstance(content, list):
            content = [content]
        obj.content = content
        obj.save()
        return Response(obj.content)

    def get(self, request, **kwargs):
        """
        获取购物网车
        """
        obj, ok = m.Cart.objects.get_or_create(user=request.user)
        return Response(obj.content)


class DocumentsViewSet(ViewSet):
    """
    文档
    """

    @para_ok_or_400(
        [
            {"name": "search", "description": "搜索"},
            {
                "name": "projectId",
                "method": V.project,
                "description": "所属项目ID",
                "replace": "project",
            },
            {"name": "type", **V.make(const.DOCUMENTS)},
        ]
    )
    def list(self, request, project=None, search=None, type=None, **kwargs):
        """获取文档列表"""
        query = dict()
        type and query.update(type=type)
        obj = m.Documents.objects.filter(**query).order_by("-id")
        if project:
            obj = obj.filter(Q(project=project) | Q(projectlog__project=project))
        if search:
            obj = obj.filter(Q(name__contains=search))
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400(
        [
            {"name": "file", "description": "文件", "type": "file", "method": V.file},
            {
                "name": "projectId",
                "method": V.project,
                "description": "所属项目ID",
                "replace": "project",
            },
            {"name": "type", **V.make(const.DOCUMENTS)},
        ]
    )
    def create(self, request, file=None, type=None, project=None, **kwargs):
        """新建文档"""
        FileBrowser.createFile(project, type, file)
        return self.result_class(data={})()

    @para_ok_or_400(
        [{"name": "pk", "description": "ID", "type": "file", "method": V.documents}]
    )
    def destroy(self, request, obj=None, **kwargs):
        """新建文档"""
        obj = obj[0]
        obj.delete()
        return self.result_class(data=obj)(serialize=True)


def _get_directory_from_path(project, path, index=None):
    paths = path.split("/")
    base_directory = m.Directory.objects.get(project=project, name=paths[0])
    for path in paths[1:index]:
        base_directory = m.Directory.objects.get(parent=base_directory, name=path)
    return base_directory


class MediaDownLoadView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        request = self.request
        path = request.GET["path"]
        project = m.Project.objects.get(id=kwargs["projectId"])
        directory = _get_directory_from_path(project, path, index=-1)
        name = path.split("/")[-1]
        obj = m.Media.objects.get(directory=directory, name=name)
        return obj.file.url


class MediaViewSet(ViewSet):
    """
    文档
    """

    serializer_class = Serializer(m.Media)

    @para_ok_or_400(
        [
            {"name": "search", "description": "搜索"},
            {"name": "path", "description": "文件路径"},
            {
                "name": "projectId",
                "method": V.project,
                "description": "所属项目ID",
                "replace": "project",
            },
            {"name": "type", **V.make(const.DOCUMENTS)},
        ]
    )
    def list(self, request, project=None, search=None, type=None, path="", **kwargs):
        """获取文档列表"""
        if path:
            dir = _get_directory_from_path(project, path)
            files = dir.files.all()
            dirs = dir.dirs.all()
        else:
            dirs = m.Directory.objects.filter(project=project, parent__isnull=True)
            files = []
        result = [
            dict(
                timestamp=1493908313,
                type="dir",
                path=getPath(path, x.name),
                filename=x.name,
                dirname="",
                basename=x.name,
            )
            for x in dirs
        ]
        result.extend(
            [
                dict(
                    type="file",
                    basename=x.name,
                    dirname="",
                    path=getPath(path, x.name),
                    **getExtension(x.name)
                )
                for x in files
            ]
        )
        return Response(result)

    @para_ok_or_400(
        [
            {"name": "file", "description": "文件", "type": "file", "method": V.file},
            {"name": "path", "description": "文件路径"},
            {
                "name": "projectId",
                "method": V.project,
                "description": "所属项目ID",
                "replace": "project",
            },
            {"name": "type", **V.make(const.DOCUMENTS)},
        ]
    )
    def create(self, request, file=None, project=None, type=None, path="", **kwargs):
        """新建文档"""
        file = request.data.get("file")
        if not file:
            return self.result_class().error("file", "不能为空")
        directory = getDirectory(path, project)
        file = File(file)
        obj = m.Media.objects.create(name=file.name, file=file, directory=directory)
        return self.result_class(data=obj)(serialize=True)


def getDirectory(path, project):
    path = path.split("/", 1)
    dir, ok = m.Directory.objects.get_or_create(name=path[0], project=project)
    if len(path) > 1:
        return getDirectory(path[1], project)
    return dir


def getExtension(filename):
    return dict(ext=filename.split(".")[-1])


def getPath(path, filename):
    if not path:
        return filename
    return "/".join((path, filename))


class DirectoryViewSet(ViewSet):
    """
    文档目录
    """

    serializer_class = Serializer(m.Directory)

    @para_ok_or_400(
        [
            {"name": "search", "description": "搜索"},
            {
                "name": "projectId",
                "method": V.project,
                "description": "所属项目ID",
                "replace": "project",
            },
        ]
    )
    def list(self, request, project=None, search=None, type=None, **kwargs):
        """获取文档列表"""
        query = dict()
        obj = m.Directory.objects.filter(**query).order_by("-id")
        project and query.update(project=project)
        if search:
            obj = obj.filter(Q(name__contains=search))
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400(
        [
            {
                "name": "projectId",
                "method": V.project,
                "description": "项目ID",
                "replace": "project",
                "required": True,
            },
            {"name": "name", "description": "文件", "required": True},
            {"name": "parent", "description": "父级目录"},
        ]
    )
    def create(self, request, name=None, parent=None, project=None, **kwargs):
        """
        新建目录
        """
        paras = dict(project=project, name=name)
        if parent:
            parent, ok = m.Media.objects.get_or_create(project=project, name=parent)
            paras.update(parent=parent)
        obj, ok = m.Media.objects.get_or_create(**paras)
        return self.result_class(obj)(serialize=True)

    @para_ok_or_400(
        [{"name": "pk", "method": V.directory, "description": "目录ID", "replace": "obj"}]
    )
    @perm_ok_or_403(
        [
            {
                "method": lambda r, k: r.user.has_permission(k["obj"]),
                "reason": "无权限删除此项目组",
            }
        ]
    )
    def destroy(self, request, obj=None, **kwargs):
        """
        删除目录
        """
        obj.delete()
        return self.result_class(obj)(serialize=True)


class ProjectGroupViewSet(ViewSet):
    serializer_class = Serializer(m.ProjectGroup, dep=0)
    permission_classes = (IsAuthenticated,)

    @para_ok_or_400([{"name": "search", "description": "项目组搜索"}])
    def list(self, request, search="", **kwargs):
        """
        获取所有项目组
        """
        query = dict()
        search and query.update(name__contains=search)
        objs = m.ProjectGroup.objects.filter(**query, user=request.user)
        return self.result_class(objs)(serialize=True)

    @para_ok_or_400(
        [{"name": "name", "method": V.name, "description": "项目组名称", "required": True}]
    )
    def create(self, request, name=None, **kwargs):
        """
        新建项目组
        """
        obj, ok = ProjectGroup.objects.get_or_create(name=name, user=request.user)
        return self.result_class(obj)(serialize=True)

    @para_ok_or_400(
        [
            {
                "name": "id",
                "method": V.projectGroup,
                "description": "项目组ID",
                "replace": "obj",
            },
            {
                "name": "name",
                "method": V.name,
                "description": "项目组名称",
                "required": True,
            },
        ]
    )
    @perm_ok_or_403(
        [
            {
                "method": lambda r, k: r.user.has_permission(k["obj"]),
                "reason": "无权限编辑此项目组",
            }
        ]
    )
    def update(self, request, obj=None, **kwargs):
        """
        编辑项目组
        """
        [setattr(obj, k, v) for k, v in kwargs.items() if v]
        obj.save()
        return self.result_class(obj)(serialize=True)

    @para_ok_or_400(
        [
            {
                "name": "pk",
                "method": V.projectGroup,
                "description": "项目组ID",
                "replace": "obj",
            }
        ]
    )
    @perm_ok_or_403(
        [
            {
                "method": lambda r, k: r.user.has_permission(k["obj"]),
                "reason": "无权限删除此项目组",
            }
        ]
    )
    def destroy(self, request, obj=None, **kwargs):
        """
        删除项目组
        """
        obj.delete()
        return self.result_class(obj)(serialize=True)

    @para_ok_or_400(
        [
            {
                "name": "pk",
                "method": V.projectGroup,
                "description": "项目组ID",
                "replace": "obj",
            }
        ]
    )
    @perm_ok_or_403(
        [
            {
                "method": lambda r, k: r.user.has_permission(k["obj"]),
                "reason": "无权限查看此项目组",
            }
        ]
    )
    def retrieve(self, request, obj=None, **kwargs):
        """
        删除部门
        """
        return self.result_class(obj)(serialize=True)
