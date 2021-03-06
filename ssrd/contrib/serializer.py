from django.conf import settings
from rest_framework import serializers

from ssrd import const
from ssrd.users.filebrowser import FileBrowser
from ssrd.users.models import Group, User

ProjectType = dict(const.ProjectType)
_methodMap = {
    "created": lambda x: x.strftime(settings.REST_FRAMEWORK["DATE_FORMAT"]),
    "updated": lambda x: x.strftime(settings.REST_FRAMEWORK["DATETIME_FORMAT"]),
}


def to_repr(data):
    return {x: _methodMap.get(x, lambda x: x)(y) for x, y in data.items()}


class ProjectLogSerializer(serializers.BaseSerializer):
    def to_representation(self, o):
        return dict(
            project=ProjectSerializer(o.project).data,
            id=o.id,
            created=o.created,
            updated=o.updated,
            action=o.action,
            content=o.content,
            attatchment=[FileBrowser.getFile(o.project, x) for x in o.attatchment.all()],
        )


class ProjectSerializer(serializers.BaseSerializer):
    def to_representation(self, o):
        return dict(
            id=o.id,
            name=o.name,
            type=ProjectType[o.type],
            content=o.content,
            mobile=o.mobile,
            status=o.status,
            linkman=o.linkman,
            budget=o.budget,
            address=o.address,
            company=o.company,
            created=o.created,
            updated=o.updated,
            user=dict(username=o.user.username, id=o.user.id),
        )


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        exclude = []


class UserSerializer(serializers.ModelSerializer):
    group = GroupSerializer()

    class Meta:
        exclude = ["password"]
        model = User


def modelFactory(Model, extra, dep):
    class factory(serializers.ModelSerializer):
        class Meta:
            model = Model
            if extra:
                fields = [x.name for x in Model._meta.fields] + (extra or [])
            else:
                exclude = []
            # dep 和depth重名的时候会报错
            if dep is not None:
                depth = dep
            else:
                depth = 1

        def to_representation(self, instance):
            if hasattr(instance, "data"):
                return to_repr(instance.data())
            return super(factory, self).to_representation(instance)

    return factory


def Serializer(Model, extra=None, dep=None):
    if not hasattr(Model, "_meta"):
        return
    factory = modelFactory(Model, extra, dep)
    factory.__name__ = Model._meta.object_name + "Serializer"
    return factory
