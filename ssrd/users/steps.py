from ssrd import const
from .models import Audit, User
projectStatus = const.projectStatus


def getAudits():
    obj = Audit.objects.first()
    users = User.objects.filter(id__in=obj.steps)
    return users


Audits = getAudits()


class Step(object):
    def __init__(self, step):
        self.step = step
        self.name = projectStatus[step]

    def ok(self, group, role):
        return True

    def next(self):
        step = self.step + 1
        if step not in projectStatus:
            step = 0
        return Step(step)

    def prev(self):
        step = self.step - 1
        if step not in projectStatus:
            step = 0
        return Step(step)

    @classmethod
    def steps(cls, group, role):
        return