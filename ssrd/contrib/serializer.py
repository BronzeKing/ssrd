from rest_framework import serializers
from django.conf import settings

_methodMap = {
    'created': lambda x: x.strftime(settings.REST_FRAMEWORK['DATE_FORMAT']),
    'updated': lambda x: x.strftime(settings.REST_FRAMEWORK['DATETIME_FORMAT'])
}


def to_repr(data):
    return {x: _methodMap.get(x, lambda x: x)(y) for x, y in data.items()}


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
            if hasattr(instance, 'data'):
                return to_repr(instance.data())
            return super(factory, self).to_representation(instance)

    return factory


def Serializer(Model, extra=None, dep=None):
    if not hasattr(Model, '_meta'):
        return
    factory = modelFactory(Model, extra, dep)
    factory.__name__ = Model._meta.object_name + 'Serializer'
    return factory
