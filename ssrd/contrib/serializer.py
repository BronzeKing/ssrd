from rest_framework import serializers
from ssrd.home import models as home


# class FAQsSerializer(serializers.ModelSerializer):
    # class Meta:
        # model = home.FAQs
        # exclude = ()


def Serializer(Model):
    class factory(serializers.ModelSerializer):
        class Meta:
            model = Model
            exclude = ()
    factory.__name__ = Model._meta.object_name + 'Serializer'
    return factory
