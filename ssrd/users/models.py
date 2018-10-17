import binascii
import os
from functools import partial

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, UserManager as BaseUserManager, Group
from django.contrib.postgres.fields import JSONField
from django.core.files import File
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from ssrd import const


def isCustom(self):
    return self.name == "客户"


Group.isCustom = isCustom


def generate_key(bit=None):
    if not bit:
        return binascii.hexlify(os.urandom(20)).decode()
    return binascii.hexlify(os.urandom(20)).decode()[:bit]


def defaultProjectGroup():
    obj, ok = ProjectGroup.objects.get_or_create(name="默认")
    return obj.id
class UserManager(BaseUserManager):
    def create_user(self, username=None, email=None, password=None, **kwargs):
        if 'mobile' in kwargs and not username:
            username = kwargs['mobile']
        group, ok = Group.objects.get_or_create(name='客户')
        return self._create_user(username, email, password, group=group, **kwargs)



class User(AbstractBaseUser):
    email = models.EmailField(_("email address"), blank=True, default="")
    username = models.CharField(
        _("username"),
        max_length=150,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        error_messages={"unique": _("A user with that username already exists.")},
    )
    mobile = models.CharField(_("Mobile Phone"), unique=True, max_length=11)
    role = models.SmallIntegerField("用户权限", choices=const.ROLES, default=2)
    created = models.DateTimeField(_("date joined"), default=timezone.now)
    status = models.SmallIntegerField("状态", choices=const.STATUS, default=1)
    group = models.ForeignKey(
        Group,
        verbose_name=_("groups"),
        blank=True,
        help_text=_(
            "The groups this user belongs to. A user will get all permissions "
            "granted to each of their groups."
        ),
        related_name="user_set",
        related_query_name="user",
        on_delete=models.CASCADE,
    )
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "mobile"
    REQUIRED_FIELDS = []
    objects = UserManager()

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

    def has_permission(self, other, **kwargs):
        if not isinstance(other, models.Model):
            return False
        o = other._meta.object_name.lower()
        if o == "user":
            return True
        if o == "authorizecode":
            return True
        return True

    def create_profile(self):
        Profile.objects.get_or_create(user=self, name=self.username)

    def __str__(self):
        return "<User: {}, {}>".format(self.username, self.email)

    __repr__ = __str__


def avator():
    from django.core.files import File

    avatorPath = str(settings.APPS_DIR) + "/static/images/avator.png"
    return File(open(avatorPath, "rb"))


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="所属用户")
    avator = models.ImageField("系统结构", default=avator)
    name = models.CharField("真实姓名", max_length=50)
    gender = models.CharField("性别", choices=const.GENDER, max_length=10, default="male")
    birthday = models.DateField("生日", auto_now=True)
    company = models.CharField("所属公司", max_length=255, null=True)
    position = models.CharField("职位", null=True, max_length=255)
    qq = models.CharField("QQ号码", null=True, max_length=20)
    address = models.CharField("地址", null=True, max_length=255)
    code = models.CharField("邀请码", max_length=40, default=generate_key)

    def __str__(self):
        return "<Profile: {}>".format(self.user)

    __repr__ = __str__

    class Meta:
        unique_together = ("user",)


class Cart(models.Model):
    """购物车"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="所属用户")
    content = JSONField("内容", default=[])

    def __str__(self):
        return "<Cart: {}, {}>".format(self.user, self.content)

    __repr__ = __str__


class Order(models.Model):
    """订单"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="所属用户")
    content = JSONField("内容", default=[])
    code = models.CharField("订单号", max_length=40, default=generate_key)
    created = models.DateTimeField("创建时间", auto_now_add=True, null=True)
    updated = models.DateTimeField("更新时间", auto_now=True)

    def __str__(self):
        return "<order: {}, {}>".format(self.user, self.content)

    __repr__ = __str__


class AuthorizeCode(models.Model):
    name = models.CharField("授权码名称", max_length=50)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="授权码对应用户",
        related_name="authorizecode",
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="所属用户",
        related_name="authorizecodes",
    )
    code = models.CharField("授权码", max_length=40, default=partial(generate_key, bit=6))
    status = models.SmallIntegerField("授权码状态", choices=const.STATUS, default=1)
    created = models.DateTimeField("创建时间", auto_now_add=True, null=True)
    updated = models.DateTimeField("更新时间", auto_now=True)

    def generateUser(self):
        username = self.name
        group, ok = Group.objects.get_or_create(name="客户")
        email = self.name + "@szssrd.com",
        self.user = User.objects.create(
            username=username,
            email="",
            mobile=str(hash(email))[:11],
            password=self.code,
            group=group,
        )
        return self

    def __str__(self):
        return "<AuthorizeCode: {}, {}, {}, {}>".format(
            self.user, self.creator, self.code, self.status
        )

    __repr__ = __str__


class Invitation(models.Model):
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="邀请码所属用户",
        related_name="invitations",
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="invited",
        verbose_name="受邀用户",
    )
    created = models.DateTimeField("创建时间", auto_now_add=True, null=True)
    updated = models.DateTimeField(("更新时间"), auto_now=True)

    def __str__(self):
        return "<Invitation: {}, {}, {}>".format(self.creator, self.user)

    __repr__ = __str__


class ProjectGroup(models.Model):
    name = models.CharField("项目组", max_length=50)
    created = models.DateTimeField("创建时间", auto_now_add=True, null=True)
    updated = models.DateTimeField("更新时间", auto_now=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="所属用户",
        related_name="projectGroups",
        default=6,
    )

    class Meta:
        unique_together = ("name", "user")

    def __str__(self):
        return "<{}: {}>".format(self.name, self.created)

    __repr__ = __str__


class Project(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="所属用户",
        related_name="projects",
        default=1,
    )
    group = models.ForeignKey(
        ProjectGroup,
        on_delete=models.CASCADE,
        verbose_name="所属项目组",
        related_name="projects",
        default=defaultProjectGroup,
    )
    name = models.CharField("项目名称", max_length=50)
    type = models.CharField(
        "项目类型", choices=const.ProjectType, max_length=20, default="create"
    )
    content = JSONField("内容", default=[])
    mobile = models.CharField(_("Mobile Phone"), blank=True, default="", max_length=11)
    status = models.SmallIntegerField("项目状态", choices=const.ProjectStatus, default=1)
    remark = models.TextField("补充说明")
    duration = models.SmallIntegerField("工期", default=1)
    budget = models.SmallIntegerField("工期", default=1)
    linkman = models.CharField("联系人", max_length=50)
    address = models.CharField("地址", null=True, max_length=255)
    attatchment = models.ManyToManyField("users.Documents", verbose_name="附件")
    company = models.CharField("所属公司", max_length=255, null=True)
    created = models.DateTimeField("创建时间", auto_now_add=True, null=True)
    updated = models.DateTimeField(("更新时间"), auto_now=True)

    class Meta:
        unique_together = ("user", "name")

    def __str__(self):
        return "<{}: {}>".format(self.name, self.status)

    __repr__ = __str__


class ProjectLog(models.Model):
    project = models.ForeignKey(
        "users.Project",
        on_delete=models.CASCADE,
        verbose_name="所属项目",
        related_name="logs",
    )
    action = models.SmallIntegerField("行为", choices=const.ProjectLog, default=0)
    content = JSONField("内容")
    created = models.DateTimeField("创建时间", auto_now_add=True)
    updated = models.DateTimeField(("更新时间"), auto_now=True)
    attatchment = models.ManyToManyField("users.Documents", verbose_name="附件")

    def __str__(self):
        return "<ProjectLog: {}, {}, {}>".format(
            self.project, self.action, self.content
        )

    __repr__ = __str__


class Collected(models.Model):
    product = models.ForeignKey(
        "home.Product", on_delete=models.CASCADE, verbose_name="收藏的产品"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="所属用户",
        related_name="collects",
    )
    created = models.DateTimeField("创建时间", auto_now_add=True, null=True)
    updated = models.DateTimeField(("更新时间"), auto_now=True)

    def __str__(self):
        return "<Collect: {}, {}>".format(self.user, self.product)

    __repr__ = __str__


class Message(models.Model):
    userId = models.IntegerField("所属用户")
    title = models.TextField("标题")
    content = models.TextField("内容")
    created = models.DateTimeField("创建时间", auto_now_add=True)
    category = models.SmallIntegerField("消息类型", choices=const.MESSAGE, default=0)
    read = models.SmallIntegerField("已读", choices=const.READ, default=0)
    rank = models.IntegerField("排序", default=100)

    def __str__(self):
        return "<Message: {}, {}>".format(self.user, self.title)

    __repr__ = __str__


class Directory(models.Model):
    name = models.CharField("文件名", max_length=255, default="")
    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="dirs"
    )
    project = models.ForeignKey("users.Project", on_delete=models.CASCADE)
    updated = models.DateTimeField("更新时间", auto_now=True)

    def __str__(self):
        return "<Directory: {} {}>".format(self.parent, self.name)

    __repr__ = __str__

    class Meta:
        unique_together = ("parent", "name")


class Media(models.Model):
    type = models.SmallIntegerField("文件类型", choices=const.DOCUMENTS, default=1)
    file = models.FileField("文件", max_length=512)
    updated = models.DateTimeField("更新时间", auto_now=True)
    name = models.CharField("文件名", max_length=512, default="")
    directory = models.ForeignKey(
        Directory, on_delete=models.CASCADE, related_name="files"
    )

    def __str__(self):
        return "<Media: {}   {}>".format(self.directory, self.name)

    class Meta:
        unique_together = ("directory", "name")

    __repr__ = __str__


class Documents(models.Model):
    name = models.CharField("文件名", max_length=255, default="")
    file = models.FileField("文件")
    type = models.SmallIntegerField("文件类型", choices=const.DOCUMENTS, default=1)
    created = models.DateField("创建时间", auto_now_add=True)
    updated = models.DateTimeField("更新时间", auto_now=True)

    def __str__(self):
        return "<Documents: {}   {}>".format(self.file, self.updated)

    __repr__ = __str__

    @classmethod
    def bulk(cls, files):
        files = [File(x) for x in files]
        return cls.objects.bulk_create([cls(file=x, name=x.name) for x in files])


class Config(models.Model):
    steps = JSONField("审核步骤")  # [15, 24]  存放userId
