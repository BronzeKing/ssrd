# encoding: utf-8
from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import ugettext_lazy as _

from ssrd import const


class ProjectGroup(models.Model):
    name = models.CharField("项目组", max_length=50)
    created = models.DateTimeField("创建时间", auto_now_add=True, null=True)
    updated = models.DateTimeField("更新时间", auto_now=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="所属用户", related_name="projectGroups"
    )

    class Meta:
        unique_together = ("name", "user")

    def __str__(self):
        return "<{}: {}>".format(self.name, self.created)

    __repr__ = __str__


class Project(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="所属用户", related_name="projects", default=1
    )
    group = models.ForeignKey(ProjectGroup, on_delete=models.CASCADE, verbose_name="所属项目组", related_name="projects")
    name = models.CharField("项目名称", max_length=50)
    type = models.CharField("项目类型", choices=const.ProjectType, max_length=20, default="create")
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
    project = models.ForeignKey("users.Project", on_delete=models.CASCADE, verbose_name="所属项目", related_name="logs")
    action = models.SmallIntegerField("行为", choices=const.ProjectLog, default=0)
    content = JSONField("内容")
    created = models.DateTimeField("创建时间", auto_now_add=True)
    updated = models.DateTimeField(("更新时间"), auto_now=True)
    attatchment = models.ManyToManyField("users.Documents", verbose_name="附件")

    def __str__(self):
        return "<ProjectLog: {}, {}, {}>".format(self.project, self.action, self.content)

    __repr__ = __str__


class ProjectPermission(models.Model):
    project = models.ForeignKey("users.Project", on_delete=models.CASCADE, verbose_name="所属项目")
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, verbose_name="所属用户")
    permission = models.SmallIntegerField("权限", choices=const.ProjectPermission, default=1)

    def __str__(self):
        return "<ProjectLog: {}, {}, {}>".format(self.project, self.action, self.content)

    __repr__ = __str__
