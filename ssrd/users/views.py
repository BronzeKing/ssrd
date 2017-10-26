from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import RedirectView
from django.db.models import Q
from paraer import para_ok_or_400, perm_ok_or_403
from rest_framework.permissions import IsAuthenticated

from ssrd import const
from ssrd.contrib import APIView, UnAuthView, V, ViewSet
from ssrd.contrib.serializer import Serializer
from ssrd.contrib import serializer

from .models import AuthorizeCode, Collect, Invitation, Message, Profile, Project, User


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return '{}/{}'.format('/users', self.request.user.id)


@para_ok_or_400([{
    'name': 'role',
    'method': V.role,
    'description': ("用户角色, 默认为4，即常规用户", ) + const.ROLES
}, {
    'name': 'email',
    'method': V.email,
    'required': True,
    'description': '用户邮箱'
}, {
    'name': 'password',
    'method': V.password,
    'required': True,
    'description': '用户密码'
}, {
    'name': 'username',
    'method': V.name,
    'required': True,
    'description': '用户名'
}])
def post(self,
         request,
         username=None,
         role=4,
         email=None,
         password=None,
         **kwargs):
    result = self.result_class()
    if role < getattr(request.user, 'role', -10):  # 可以为匿名用户
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
    serializer_class = Serializer(User)

    post = post
    post.__doc__ = '新建用户'


class UserViewSet(ViewSet):
    serializer_class = Serializer(User)
    permission_classes = (IsAuthenticated, )

    @para_ok_or_400([{
        'name': 'role',
        'method': V.role,
        'description': ("用户角色过滤", ) + const.ROLES
    }, {
        'name': 'status',
        'method': V.Status,
        'description': ("用户状态过滤", ) + const.STATUS
    }, {
        'name': 'search',
        'description': '按名称搜索',
    }])
    def list(self, request, role=None, search=None, status=None, **kwargs):
        """"""
        query = dict()
        role and query.update(role=role)
        status in (0, 1) and query.update(is_active=status)
        obj = User.objects.filter(**query).order_by('-id')
        if search:
            obj = obj.filter(Q(username__contains=search) | Q(email__contains=search) | Q(mobile__contains=search))
        return self.result_class(data=obj)(serialize=True)

    create = post

    @para_ok_or_400([{
        'name': 'pk',
        'method': V.user,
        'description': '用户ID',
        'replace': 'user'
    }, {
        'name': 'username',
        'method': V.name,
        'description': '用户名称'
    }, {
        'name': 'email',
        'method': V.email,
        'description': '用户邮箱'
    }, {
        'name': 'status',
        'method': V.Status,
        'description': ("用户状态过滤", ) + const.STATUS
    }])
    @perm_ok_or_403([{
        'method': lambda r, k: r.user.has_permission(k['user']),
        'reason': '无权限'
    }])
    def update(self,
               request,
               user=None,
               username=None,
               status=None,
               email=None,
               **kwargs):
        """更新用户"""
        username and setattr(user, 'username', username)
        email and setattr(user, 'email', email)
        status in (0, 1) and setattr(user, 'is_active', status)
        user.save()
        return self.result_class(user)(serialize=True)

    @para_ok_or_400([{
        'name': 'pk',
        'method': V.user,
        'description': '用户ID',
        'replace': 'user'
    }])
    @perm_ok_or_403([{
        'method': lambda r, k: r.user.has_permission(k['user']),
        'reason': '无权限'
    }])
    def destroy(self, request, user, **kwargs):
        """
        删除用户
        """
        user.delete()
        return self.result_class().data(user)(serialize=True)

    @para_ok_or_400([{
        'name': 'pk',
        'method': V.user,
        'description': '用户ID',
        'replace': 'user'
    }])
    @perm_ok_or_403([{
        'method': lambda r, k: r.user.has_permission(k['user']),
        'reason': '无权限'
    }])
    def retrieve(self, request, user, **kwargs):
        """
        获取用户
        """
        return self.result_class().data(user)(serialize=True)


class ProfileView(APIView):
    serializer_class = Serializer(Profile)

    @para_ok_or_400([{
        'name': 'user',
        'method': V.user,
        'description': '用户ID',
    }])
    def get(self, request, user=None, **kwargs):
        return self.result_class().data(user.profile)()

    @para_ok_or_400([{
        'name': 'user',
        'method': V.user,
        'description': '用户ID',
    }, {
        'name': 'gender',
        'method': V.gender,
        'description': "性别",
    }, {
        'name': 'name',
        'description': '真实姓名',
        'method': V.name
    }, {
        'name': 'birthday',
        'description': '生日',
        'method': V.date,
    }, {
        'name': 'company',
        'description': '所属公司',
        'method': V.name,
    }, {
        'name': 'position',
        'description': '职位',
        'method': V.name,
    }, {
        'name': 'qq',
        'description': 'QQ号码',
        'method': V.num
    }, {
        'name': 'address',
        'description': '地址',
        'method': V.name
    }])
    def post(self, request, **kwargs):
        profile = request.user.profile
        [setattr(profile, k, v) for k, v in kwargs.items() if v]
        profile.save()
        return self.result_class(data=profile)()


class AuthorizeCodeViewSet(ViewSet):
    serializer_class = Serializer(AuthorizeCode)

    @para_ok_or_400([{
        'name': 'user',
        'method': V.user,
        'description': '用户ID',
    }])
    def list(self, request, user=None, **kwargs):
        query = dict()
        request.user.role > 0 and query.update(creator=request.user)
        acs = AuthorizeCode.objects.filter(**query)
        return self.result_class(data=acs)(serialize=True)

    def create(self, request, **kwargs):
        """新建授权码"""
        obj = AuthorizeCode(creator=request.user).generateUser()
        obj.save()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400([{
        'name': 'pk',
        'method': V.authorizecode,
        'description': '授权码ID',
        'replace': 'obj'
    }, {
        'name': 'status',
        'method': V.num,
        'description': ("授权码状态过滤", ) + const.STATUS
    }])
    @perm_ok_or_403([{
        'method': lambda r, k: r.user.has_permission(k['obj']),
        'reason': '无权限更改此授权码'
    }])
    def update(self, request, obj=None, status=None, **kwargs):
        """更新授权码"""
        obj.statsu = status
        obj.save()
        return self.result_class(obj)(serialize=True)

    @para_ok_or_400([{
        'name': 'pk',
        'method': V.authorizecode,
        'description': '授权码ID',
        'replace': 'obj'
    }])
    @perm_ok_or_403([{
        'method': lambda r, k: r.user.has_permission(k['obj']),
        'reason': '无权限更改此授权码'
    }])
    def destroy(self, request, obj=None, status=None, **kwargs):
        """删除授权码"""
        obj.delete()
        return self.result_class(obj)(serialize=True)

    @para_ok_or_400([{
        'name': 'pk',
        'method': V.authorizecode,
        'description': '授权码ID',
        'replace': 'obj'
    }])
    @perm_ok_or_403([{
        'method': lambda r, k: r.user.has_permission(k['obj']),
        'reason': '无权限更改此授权码'
    }])
    def retrieve(self, request, obj=None, **kwargs):
        """获取单个授权码"""
        return self.result_class(obj)(serialize=True)


class InvitationViewSet(ViewSet):
    serializer_class = Serializer(Invitation)

    @para_ok_or_400([{
        'name': 'user',
        'method': V.user,
        'description': "所属用户过滤"
    }])
    def list(self, request, user=None, **kwargs):
        """
        获取受登录用户邀请的用户列表
        """
        query = dict()
        request.user.role == 0 and user and query.update(creator=request.user)
        its = Invitation.objects.filter(**query)
        return self.result_class(data=its)(serialize=True)


class ProjectViewSet(ViewSet):
    serializer_class = Serializer(Project)

    @para_ok_or_400([{
        'name': 'stats',
        'method': V.status,
        'description': ("项目状态过滤", ) + const.ORDER_STATUS
    }, {
        'name': 'search',
        'description': '名称搜索过滤'
    }])
    def list(self, request, status=None, search=None, **kwargs):
        """
        获取受登录用户有权限的项目
        """
        user = request.user
        query = dict()
        user.role > 0 and query.update(user=user)  # 管理员获取全量
        search and query.update(name=search)
        status and query.update(status=status)
        dataset = Project.objects.filter(**query).select_related('user')
        return self.result_class(data=dataset)(serialize=True)

    @para_ok_or_400([{
        'name': 'name',
        'description': '项目名称',
        'method': V.name,
        'required': True
    }, {
        'name': 'picture',
        'description': '背景图片',
        'required': True,
        'method': V.file,
        'type': 'file'
    }])
    def create(self, request, name=None, picture=None, **kwargs):
        """新建项目"""
        data = dict(name=name, user=request.user, picture=picture)
        obj = Project.objects.create(**data)
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400([{
        'name': 'pk',
        'method': V.project,
        'description': '项目ID',
        'replace': 'obj'
    }, {
        'name': 'status',
        'method': V.order_status,
        'description': ("项目状态", ) + const.ORDER_STATUS
    }, {
        'name': 'name',
        'description': '项目名称',
        'method': V.name,
    }])
    @perm_ok_or_403([{
        'method': lambda r, k: r.user.has_permission(k['obj']),
        'reason': '无权限更改此项目'
    }])
    def update(self, request, obj=None, name=None, status=None, **kwargs):
        """更新授权码"""
        status and setattr(obj, 'status', status)
        name and setattr(obj, 'name', name)
        obj.save()
        return self.result_class(obj)(serialize=True)

    @para_ok_or_400([{
        'name': 'pk',
        'method': V.project,
        'description': '项目ID',
        'replace': 'obj'
    }])
    @perm_ok_or_403([{
        'method': lambda r, k: r.user.has_permission(k['obj']),
        'reason': '无权限删除此项目'
    }])
    def destroy(self, request, obj=None, status=None, **kwargs):
        """删除项目"""
        obj.delete()
        return self.result_class(obj)(serialize=True)

    @para_ok_or_400([{
        'name': 'pk',
        'method': V.project,
        'description': '项目ID',
        'replace': 'obj'
    }])
    @perm_ok_or_403([{
        'method': lambda r, k: r.user.has_permission(k['obj']),
        'reason': '无权限查看此项目'
    }])
    def retrieve(self, request, obj=None, **kwargs):
        """获取单个项目"""
        return self.result_class(obj)(serialize=True)


class CollectViewSet(ViewSet):
    serializer_class = Serializer(Collect, dep=0)

    def list(self, request):
        """
        获取登录用户的收藏列表
        """
        query = dict()
        request.user.role > 0 and query.update(user=request.user)
        objs = Collect.objects.filter(**query)
        return self.result_class(objs)(serialize=True)

    @para_ok_or_400([{
        'name': 'productId',
        'method': V.product,
        'description': '产品ID',
        'replace': 'obj',
        'required': True
    }])
    def create(self, request, obj=None, **kwargs):
        """
        新建收藏
        """
        if not request.user.is_authenticated:
            request.user = User.objects.first()
        obj, ok = Collect.objects.get_or_create(user=request.user, product=obj)
        return self.result_class(obj)(serialize=True)

    @para_ok_or_400([{
        'name': 'pk',
        'method': V.collect,
        'description': '收藏品ID',
        'replace': 'obj'
    }])
    @perm_ok_or_403([{
        'method': lambda r, k: r.user.has_permission(k['obj']),
        'reason': '无权限删除此收藏'
    }])
    def destroy(self, request, obj=None, **kwargs):
        """
        删除收藏
        """
        obj.delete()
        return self.result_class(obj)(serialize=True)

    @para_ok_or_400([{
        'name': 'pk',
        'method': V.collect,
        'description': '收藏品ID',
        'replace': 'obj'
    }])
    @perm_ok_or_403([{
        'method': lambda r, k: r.user.has_permission(k['obj']),
        'reason': '无权限删除此收藏'
    }])
    def retrieve(self, request, obj=None, **kwargs):
        """
        删除收藏
        """
        return self.result_class(obj)(serialize=True)


class MessageViewSet(ViewSet):
    permission_classes = (IsAuthenticated, )
    serializer_class = Serializer(Message, dep=0)

    @para_ok_or_400([{
        'name': 'read',
        'description': ("已读", ) + const.READ,
    }])
    def list(self, request, read=None, **kwargs):
        """
        获取登录用户的消息列表
        """
        query = dict(userId=request.user.id)
        read and query.update(read=read)
        objs = Message.objects.filter(**query).order_by('rank', '-created')
        return self.result_class(objs)(serialize=True)

    @para_ok_or_400([{
        'name': 'userId',
        'description': '所属用户ID',
        'method': V.user
    }, {
        'name': 'title',
        'description': '标题',
        'required': True
    }, {
        'name': 'content',
        'description': '内容',
        'required': True
    }])
    def create(self, request, title=None, user=None, content=None, **kwargs):
        """
        新建消息
        """
        user = user or request.user
        obj = Message.objects.create(
            userId=user.id, title=title, content=content)
        #  obj = Message.objects.bulk_create(
        #  (Message(userId=x, title=title, content=content)
        #  for x in User.objects.filter(role__gt=10)))
        return self.result_class(obj)(serialize=True)

    @para_ok_or_400([{
        'name': 'pk',
        'method': V.message,
        'description': '消息ID',
        'replace': 'obj'
    }, {
        'name': 'title',
        'description': '消息标题',
    }, {
        'name': 'content',
        'description': '消息内容',
    }, {
        'name': 'read',
        'description': '已读',
    }])
    @perm_ok_or_403([{
        'method': lambda r, k: r.user.has_permission(k['obj']),
        'reason': '无权限修改此消息'
    }])
    def update(self, request, obj=None, **kwargs):
        """
        修改消息
        """
        [setattr(obj, k, v) for k, v in kwargs.items() if v]
        obj.save()
        return self.result_class(obj)(serialize=True)

    @para_ok_or_400([{
        'name': 'pk',
        'method': V.message,
        'description': '消息ID',
        'replace': 'obj'
    }])
    @perm_ok_or_403([{
        'method': lambda r, k: r.user.has_permission(k['obj']),
        'reason': '无权限删除此消息'
    }])
    def destroy(self, request, obj=None, **kwargs):
        """
        删除消息
        """
        obj.delete()
        return self.result_class(obj)(serialize=True)

    @para_ok_or_400([{
        'name': 'pk',
        'method': V.message,
        'description': '消息ID',
        'replace': 'obj'
    }])
    @perm_ok_or_403([{
        'method': lambda r, k: r.user.has_permission(k['obj']),
        'reason': '无权限删除此消息'
    }])
    def retrieve(self, request, obj=None, **kwargs):
        """
        获取消息
        """
        return self.result_class(obj)(serialize=True)
