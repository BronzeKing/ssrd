from rest_framework import serializers


def Serializer(Model, extra=None, dep=None):
    if not hasattr(Model, '_meta'):
        return

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
            if hasattr(self.Meta.model, 'data'):
                return instance.data()
            return super(factory, self).to_representation(instance)

    factory.__name__ = Model._meta.object_name + 'Serializer'
    return factory
