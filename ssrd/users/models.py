import os
import binascii
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.conf import settings

from ssrd import const


def generate_key():
    return binascii.hexlify(os.urandom(20)).decode()


class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_('Name of User'), blank=True, max_length=255)

    mobile = models.IntegerField(_("Mobile Phone"), blank=True, default=0)
    role = models.IntegerField("用户权限", choices=const.ROLES, default=1)

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})

    def has_permission(self, other, **kwargs):
        if not isinstance(other, models.Model):
            return False
        o = other._meta.object_name.lower()
        if o == 'user':
            return True
        if o == 'authorizecode':
            return True
        return True

    def __str__(self):
        return "<User: {}, {}>".format(self.username, self.email)

    __repr__ = __str__

    def data(self):
        return dict(
            username=self.username,
            id=self.id,
            email=self.email,
            mobile=self.mobile)


class Group(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created = models.DateTimeField("创建时间", auto_now_add=True, null=True)
    updated = models.DateTimeField("更新时间", auto_now=True)

    def __str__(self):
        return "<{}: {}>".format(self.name, self.created)

    __repr__ = __str__


class Project(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="所属用户",
        on_delete=models.CASCADE,
        related_name='projects',
        default=1)
    name = models.CharField("项目名称", max_length=50, unique=True)
    status = models.IntegerField("项目状态", choices=const.ORDER_STATUS, default=1)
    picture = models.ImageField("背景图片", null=True)
    created = models.DateTimeField("创建时间", auto_now_add=True, null=True)
    updated = models.DateTimeField(("更新时间"), auto_now=True)

    def data(self):
        return dict(
            id=self.id,
            user=self.user.data(),
            name=self.name,
            created=self.created,
            status=self.status,
            updated=self.updated)

    def __str__(self):
        return "<{}: {}>".format(self.name, self.status)

    __repr__ = __str__


class AuthorizeCode(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        verbose_name="授权码对应用户",
        related_name="authorizecode",
        on_delete=models.CASCADE)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="所属用户",
        related_name="authorizecodes")
    code = models.CharField("授权码", max_length=40, default=generate_key)
    status = models.IntegerField("授权码状态", choices=const.STATUS, default=1)
    created = models.DateTimeField("创建时间", auto_now_add=True, null=True)
    updated = models.DateTimeField("更新时间", auto_now=True)

    def generateUser(self):
        username = 'user-{}'.format(User.objects.last().id + 1)
        self.user = User.objects.create(
            username=username, email='', password='123456')
        return self

    def data(self):
        return dict(
            user=self.user.data(),
            creator=self.creator.data(),
            code=self.code,
            status=self.status,
            created=self.created,
            updated=self.updated)

    def __str__(self):
        return "<Project: {}, {}, {}, {}>".format(self.user, self.creator,
                                                  self.code, self.status)

    __repr__ = __str__


class Invitation(models.Model):
    code = models.CharField("邀请码", max_length=40, default=generate_key)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        verbose_name="邀请码对应用户",
        related_name="invitation")
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="所属用户",
        related_name="invitations")
    created = models.DateTimeField("创建时间", auto_now_add=True, null=True)
    updated = models.DateTimeField(("更新时间"), auto_now=True)

    def data(self):
        return dict(
            code=self.code,
            user=self.user.data(),
            creator=self.creator.data(),
            created=self.created,
            updated=self.updated)

    def __str__(self):
        return "<Invitation: {}, {}, {}>".format(self.user, self.creator,
                                                 self.code)

    __repr__ = __str__


class ProjectDynamics(models.Model):
    project = models.ForeignKey(
        Project, verbose_name="所属项目", related_name="projectDynamics")


class Collect(models.Model):
    project = models.ForeignKey(
        Project, verbose_name="收藏的项目", related_name="collects")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="所属用户", related_name="collects")
    created = models.DateTimeField("创建时间", auto_now_add=True, null=True)
    updated = models.DateTimeField(("更新时间"), auto_now=True)

    def data(self):
        return dict(
            id=self.id,
            project=self.project.data(),
            user=self.user.data(),
            created=self.created,
            updated=self.updated)

    def __str__(self):
        return "<Collect: {}, {}>".format(self.user, self.project)

    __repr__ = __str__


class Message(models.Model):
    userId = models.IntegerField("所属用户")
    title = models.TextField("标题")
    content = models.TextField("内容")
    created = models.DateTimeField("创建时间", auto_now_add=True)
    read = models.SmallIntegerField("已读", choices=const.READ, default=0)
    rank = models.IntegerField("排序", default=100)

    def data(self):
        return dict(
            id=self.id,
            userId=self.userId,
            title=self.title,
            content=self.content,
            read=self.read,
            created=self.created)

    def __str__(self):
        return "<Message: {}, {}>".format(self.user, self.title)

    __repr__ = __str__
