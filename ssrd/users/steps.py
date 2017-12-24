from ssrd import const
from .models import Config as AuditModel, User
projectStatus = const.projectStatus


def getAudits():
    try:
        obj = AuditModel.objects.first()
        users = [x for x in User.objects.filter(id__in=obj.steps)]
    except Exception:
        users = []
    return users


class Audit(object):
    links = getAudits()

    @classmethod
    def next(cls, user):
        try:
            index = cls.links.index(user)
        except ValueError:
            return
        if len(cls.links) < index + 1:
            return
        return cls.links[index + 1]

    @classmethod
    def prev(cls, user):
        try:
            index = cls.links.index(user)
        except ValueError:
            return
        if index - 1 < 0:
            return
        return cls.links[index - 1]


class Step(object):
    def __init__(self, step):
        """
        docstring here
            :param step: Interger
        """
        self.step = step
        self.name = projectStatus[step]

    def ok(self, user):
        return True

    def next(self, user):
        step = self.step
        if self.name == '审核':
            audit = Audit.next(user)
            if audit:
                return self
        step = self.step + 1
        return Step(step)

    def prev(self, user):
        if self.name == '驳回':
            audit = Audit.prev(user)
            if audit:
                return self
        step = self.step - 1
        return Step(step)

    def __call__(self, user, action):
        actionName = const.ProjectLogMapReverse[int(action)]
        if actionName not in projectStatus.values():
            return self
        if actionName == '驳回':
            return self.prev(user)
        return self.next(user)

    @classmethod
    def steps(cls, user):
        '''
        @group 用户组
        @role 用户权限
        '''
        result = []
        for step in projectStatus:
            step = cls(step)
            if step.ok(user):
                result.append(step)
        return result