import factory
import io
from PIL import Image


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda n: 'user-{0}'.format(n))
    email = factory.Sequence(lambda n: 'user-{0}@example.com'.format(n))
    password = factory.PostGenerationMethodCall('set_password', 'password')

    class Meta:
        model = 'users.User'
        django_get_or_create = ('username', )


class ProjectFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda n: 'name-{0}'.format(n))

    class Meta:
        model = 'users.Project'


class AuthorizeCodeFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    creator = factory.SubFactory(UserFactory)

    class Meta:
        model = 'users.AuthorizeCode'


class InvitationFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    creator = factory.SubFactory(UserFactory)

    class Meta:
        model = 'users.Invitation'


class CollectFactory(factory.django.DjangoModelFactory):
    project = factory.SubFactory(ProjectFactory)
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = 'users.Collect'


class MessageFactory(factory.django.DjangoModelFactory):
    title = factory.Sequence(lambda n: 'title-{0}'.format(n))
    content = factory.Sequence(lambda n: 'content-{0}'.format(n))
    userId = factory.Sequence(lambda n: n)

    class Meta:
        model = 'users.Message'


def FileFactory():
    file = io.BytesIO()
    image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
    image.save(file, 'png')
    file.name = 'test.png'
    file.seek(0)
    return file
