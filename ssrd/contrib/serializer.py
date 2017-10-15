from rest_framework import serializers


def Serializer(Model):
    class factory(serializers.ModelSerializer):
        class Meta:
            model = Model
            exclude = ()
            depth = 1

        def to_representation(self, instance):
            if hasattr(self.Meta.model, 'data'):
                return instance.data()
            return super(factory, self).to_representation(instance)

    #  if Model._meta.object_name == 'System':
        #  import ipdb
        #  ipdb.set_trace(context=30)

    if not hasattr(Model, '_meta'):
        return
    factory.__name__ = Model._meta.object_name + 'Serializer'
    return factory
