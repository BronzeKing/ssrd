import factory


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
