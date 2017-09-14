from rest_framework import serializers


def Serializer(Model):
    class factory(serializers.ModelSerializer):
        class Meta:
            model = Model
            exclude = ()

        def to_representation(self, instance):
            if hasattr(self.Meta.model, 'data'):
                return instance.data()
            return super(factory, self).to_representation(instance)

    factory.__name__ = Model._meta.object_name + 'Serializer'
    return factory
