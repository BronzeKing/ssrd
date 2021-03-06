import typing

from ssrd import const

from .models import Config as AuditModel
from .models import Group, Message, Project, User

projectStatus = const.projectStatus


def getAudits() -> typing.List[User]:
    try:
        obj = AuditModel.objects.first()
        users = [x for x in User.objects.filter(id__in=obj.steps)]
    except Exception:
        users = []
    return users


messageTpl = """尊敬的{}:
    项目{}需要您的处理
"""


def createMessage(user: User, status: int, project: Project):
    groupNames = const.StatusByRole.get(str(status), {}).get("group", [])
    users = list(User.objects.filter(group__name__in=groupNames))
    users += [user]
    actionStr = const.ProjectStatus[project.status]
    content = messageTpl.format(user.username, project.name)
    objs = [
        Message(title=f"{project.name} {actionStr}通知", content=content, userId=user.id)
        for user in users
    ]
    Message.objects.bulk_create(objs)


class Audit(object):
    links = getAudits()

    @classmethod
    def next(cls, user: User) -> User:
        try:
            index = cls.links.index(user)
        except ValueError:
            return
        if len(cls.links) < index + 1:
            return
        return cls.links[index + 1]

    @classmethod
    def prev(cls, user: User) -> User:
        try:
            index = cls.links.index(user)
        except ValueError:
            return None
        if index - 1 < 0:
            return None
        return cls.links[index - 1]


class Step(object):
    def __init__(self, step: int) -> None:
        """
        docstring here
            :param step: Interger
        """
        self.step = step
        self.name = projectStatus[step]

    def ok(self, user: User) -> bool:
        """
        该用户对此状态的项目是否有权限
        """
        return user.group.name in const.StatusByRole[str(self.step)]["group"]

    def next(self, user: User, project: Project = None) -> "Step":
        step = self.step
        if self.name == "审核":
            audit = Audit.next(user)
            if audit:
                return self
        step = self.step + 1
        if project:
            createMessage(user, step, project)
        return Step(step)

    def prev(self, user: User, project: Project = None) -> "Step":
        if self.name == "驳回":
            audit = Audit.prev(user)
            if audit:
                return self
        step = self.step - 1
        if project:
            createMessage(user, step, project)
        return Step(step)

    def __call__(self, user: User, action: str, project: Project = None) -> "Step":
        actionName = const.ProjectLogMapReverse[int(action)]
        if actionName not in projectStatus.values():
            return self
        if actionName == "驳回":
            return self.prev(user, project)
        return self.next(user, project)

    @classmethod
    def steps(cls, user: User) -> typing.List["Step"]:
        """
        @group 用户组
        @role 用户权限
        """
        result = []
        for _step in projectStatus:
            step = cls(_step)
            if step.ok(user):
                result.append(step)
        return result
