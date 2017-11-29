from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import RedirectView
from django.db.models import Q
from paraer import para_ok_or_400, perm_ok_or_403
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from ssrd import const
from ssrd.contrib import APIView, UnAuthView, V, ViewSet
from ssrd.contrib.serializer import Serializer
from ssrd.users import models as m

from .models import AuthorizeCode, Collected, Invitation, Message, Profile, Project, User, ProjectLog, Documents


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
        status and query.update(status=status)
        obj = User.objects.filter(**query).exclude(id=request.user.id).order_by('-id')
        if search:
            obj = obj.filter(
                Q(username__contains=search) | Q(email__contains=search) | Q(
                    mobile__contains=search))
        return self.result_class(data=obj)(serialize=True)

    create = post

    @para_ok_or_400([{
        'name': 'pk',
        'method': V.user,
        'description': '用户ID',
        'replace': 'user'
    }, {
        'name': 'group',
        'method': V.group,
        'description': '用户组ID',
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
               **kwargs):
        """更新用户"""
        [setattr(user, k, v) for k, v in kwargs.items() if v]
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
    permission_classes = (IsAuthenticated, )

    @para_ok_or_400([{
        'name': 'user',
        'method': V.user,
        'description': '用户ID',
    }])
    def get(self, request, user=None, **kwargs):
        return self.result_class().data(user.profile)(serialize=True)

    @para_ok_or_400([{
        'name': 'userId',
        'method': V.user,
        'replace': 'user',
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
    def post(self, request, userId=None, user=None, **kwargs):
        profile = request.user.profile
        [setattr(profile, k, v) for k, v in kwargs.items() if v]
        profile.save()
        return self.result_class(data=profile)(serialize=True)


class AuthorizeCodeViewSet(ViewSet):
    serializer_class = Serializer(AuthorizeCode, extra=['user'])
    permission_classes = (IsAuthenticated, )

    @para_ok_or_400([{
        'name': 'user',
        'method': V.user,
        'description': '用户ID',
    }, {
        'name': 'search',
        'description': '名称搜索过滤'
    }, {
        'name': 'status',
        'method': V.Status,
        'description': ('状态过滤', ) + const.STATUS
    }])
    def list(self, request, user=None, status=None, search=None, **kwargs):
        query = dict()
        request.user.role > 0 and query.update(creator=request.user)
        status and query.update(status=status)
        obj = AuthorizeCode.objects.filter(**query)
        if search:
            obj = obj.filter(Q(user__username__contains=search))
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400([{
        'name': 'name',
        'method': V.name,
        'description': '授权码名称'
    }])
    def create(self, request, name, **kwargs):
        """新建授权码"""
        if AuthorizeCode.objects.filter(name=name, creator=request.user):
            return self.result_class().error('name', '已存在同名的授权码')()
        obj = AuthorizeCode(name=name, creator=request.user).generateUser()
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
        obj.status = status
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
    permission_classes = (IsAuthenticated, )

    @para_ok_or_400([{
        'name': 'status',
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
        status and query.update(status=status)
        obj = Project.objects.filter(**query).select_related('user')
        if search:
            obj = obj.filter(name__contains=search)
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400([{
        'name': 'name',
        'description': '项目名称',
        'method': V.name,
        'required': True
    }, {
        'name': 'attatchment',
        'description': '项目文档',
        'method': V.files,
        'type': 'file'
    }, {
        'name': 'type',
        'description': ('项目类型', ) + const.ProjectType,
        'method': lambda x: x in dict(const.ProjectType) and x,
    }, {
        'name': 'mobile',
        'description': '手机',
        'method': V.mobile,
        'required': True
    }, {
        'name': 'linkman',
        'description': '联系人',
        'required': True
    }, {
        'name': 'address',
        'description': '项目地址',
    }, {
        'name': 'remark',
        'description': '补充说明',
    }, {
        'name': 'content',
        'description': '项目内容'
    }, {
        'name': 'budget',
        'method': V.num,
        'description': '预算'
    }, {
        'name': 'duration',
        'method': V.num,
        'description': '工期'
    }])
    def create(self, request, attatchment=None, **kwargs):
        """新建项目"""
        obj, ok = Project.objects.get_or_create(user=request.user, **kwargs)
        obj.attatchment.add(*Documents.bulk(attatchment or []))
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
        'required': True
    }, {
        'name': 'attatchment',
        'description': '项目文档',
        'method': V.files,
        'type': 'file'
    }, {
        'name': 'type',
        'description': ('项目类型', ) + const.ProjectType,
        'method': lambda x: x in dict(const.ProjectType) and x,
    }, {
        'name': 'mobile',
        'description': '手机',
        'method': V.mobile,
        'required': True
    }, {
        'name': 'linkman',
        'description': '联系人',
        'required': True
    }, {
        'name': 'address',
        'description': '项目地址',
    }, {
        'name': 'remark',
        'description': '补充说明',
    }, {
        'name': 'content',
        'method': V.json,
        'description': '项目内容'
    }, {
        'name': 'budget',
        'method': V.num,
        'description': '预算'
    }, {
        'name': 'duration',
        'method': V.num,
        'description': '工期'
    }])
    @perm_ok_or_403([{
        'method': lambda r, k: r.user.has_permission(k['obj']),
        'reason': '无权限更改此项目'
    }])
    def update(self, request, obj=None, name=None, status=None, **kwargs):
        """更新项目"""
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


class ProjectLogViewSet(ViewSet):
    serializer_class = Serializer(ProjectLog, dep=2)
    permission_classes = (IsAuthenticated, )

    @para_ok_or_400([{
        'name': 'projectId',
        'method': V.project,
        'description': '项目ID',
        'replace': 'project'
    }, {
        'name': 'action',
        'method': lambda x: x in dict(const.ProjectLog),
        'description': ("行为", ) + const.ProjectLog
    }])
    def list(self, request, project=None, action=None, **kwargs):
        """
        获取项目日志，如签证，工作日志，审核日志等
        """
        query = dict()
        project and query.update(project=project)
        action and query.update(action=action)
        obj = ProjectLog.objects.filter(**query)
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400([{
        'name': 'projectId',
        'method': V.project,
        'description': '项目ID',
        'replace': 'project'
    }, {
        'name': 'action',
        'method': lambda x: int(x) in dict(const.ProjectLog),
        'description': ("行为", ) + const.ProjectLog
    }, {
        'name': 'content',
        'description': '内容'
    }, {
        'name': 'attatchment',
        'method': V.files,
        'description': '附件，可以传list',
        'type': 'file'
    }, {
        'name': 'date',
        'method': V.date,
        'description': '工作时间'
    }])
    def create(self, request, project=None, action=None, attatchment=None, **kwargs):
        """新建项目日志"""
        obj = ProjectLog.objects.create(
            project=project, action=action, content=kwargs)
        attatchment = request.POST.getlist('attatchment', [])
        docs = Documents.bulk(attatchment)
        obj.attatchment.add(*docs)
        return self.result_class(data=obj)(serialize=True)


class CollectViewSet(ViewSet):
    serializer_class = Serializer(Collected, dep=0)
    permission_classes = (IsAuthenticated, )

    def list(self, request):
        """
        获取登录用户的收藏列表
        """
        query = dict()
        request.user.role > 0 and query.update(user=request.user)
        objs = Collected.objects.filter(**query)
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
        obj, ok = Collected.objects.get_or_create(user=request.user, product=obj)
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

class GroupViewSet(ViewSet):
    serializer_class = Serializer(m.Group, dep=0)
    permission_classes = (IsAuthenticated, )

    @para_ok_or_400([{
        'name': 'search',
        'description': '部门搜索',
    }])
    def list(self, request, search='', **kwargs):
        """
        获取所有部门
        """
        query = dict()
        search and query.update(name__contains=search)
        objs = m.Group.objects.filter(**query)
        return self.result_class(objs)(serialize=True)

    @para_ok_or_400([{
        'name': 'name',
        'method': V.name,
        'description': '部门名称',
        'required': True
    }])
    def create(self, request, **kwargs):
        """
        新建部门
        """
        obj, ok = m.Group.objects.get_or_create(**kwargs)
        return self.result_class(obj)(serialize=True)

    @para_ok_or_400([{
        'name': 'id',
        'method': V.group,
        'description': '部门ID',
        'replace': 'obj'
    }, {
        'name': 'name',
        'method': V.name,
        'description': '部门名称',
        'required': True
    }])
    @perm_ok_or_403([{
        'method': lambda r, k: r.user.has_permission(k['obj']),
        'reason': '无权限删除此部门'
    }])
    def update(self, request, obj=None, **kwargs):
        """
        编辑部门
        """
        [setattr(obj, k, v) for k, v in kwargs.items() if v]
        obj.save()
        return self.result_class(obj)(serialize=True)

    @para_ok_or_400([{
        'name': 'pk',
        'method': V.group,
        'description': '部门ID',
        'replace': 'obj'
    }])
    @perm_ok_or_403([{
        'method': lambda r, k: r.user.has_permission(k['obj']),
        'reason': '无权限删除此部门'
    }])
    def destroy(self, request, obj=None, **kwargs):
        """
        删除部门
        """
        obj.delete()
        return self.result_class(obj)(serialize=True)

    @para_ok_or_400([{
        'name': 'pk',
        'method': V.group,
        'description': '部门ID',
        'replace': 'obj'
    }])
    @perm_ok_or_403([{
        'method': lambda r, k: r.user.has_permission(k['obj']),
        'reason': '无权限删除此部门'
    }])
    def retrieve(self, request, obj=None, **kwargs):
        """
        删除部门
        """
        return self.result_class(obj)(serialize=True)

class CartView(APIView):
    serializer_class = Serializer(m.Cart, dep=0)
    permission_classes = (IsAuthenticated, )

    @para_ok_or_400([{
        'name': 'content',
        'description': '购物车内容',
        'required': True
    }])
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

    def get(self, request,  **kwargs):
        """
        获取购物网车
        """
        obj, ok = m.Cart.objects.get_or_create(user=request.user)
        return Response(obj.content)