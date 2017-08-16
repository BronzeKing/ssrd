import factory


class RecruitmentCategoryFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: 'RecruitmentCategory-{0}'.format(n))

    class Meta:
        model = 'home.RecruitmentCategory'


class ProductCategoryFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: 'RecruitmentCategory-{0}'.format(n))

    class Meta:
        model = 'home.ProductCategory'


class CharityActivityFactory(factory.django.DjangoModelFactory):
    title = factory.Sequence(lambda n: 'title-{0}'.format(n))
    content = factory.Sequence(lambda n: 'content-{0}'.format(n))

    class Meta:
        model = 'home.CharityActivity'


class ConsultationArticlesFactory(factory.django.DjangoModelFactory):
    title = factory.Sequence(lambda n: 'title-{0}'.format(n))
    content = factory.Sequence(lambda n: 'content-{0}'.format(n))

    class Meta:
        model = 'home.ConsultationArticles'


class ProductFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: 'Product-{0}'.format(n))
    category = factory.SubFactory(ProductCategoryFactory)

    class Meta:
        model = 'home.Product'


class RecruitmentFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: 'name-{0}'.format(n))
    salary = factory.Sequence(lambda n: 'salary-{0}'.format(n))
    detail = factory.Sequence(lambda n: 'detail-{0}'.format(n))
    category = factory.SubFactory(RecruitmentCategoryFactory)

    class Meta:
        model = 'home.Recruitment'


class ServicePromiseFactory(factory.django.DjangoModelFactory):
    title = factory.Sequence(lambda n: 'title-{0}'.format(n))
    content = factory.Sequence(lambda n: 'content-{0}'.format(n))
    rank = factory.Sequence(lambda n: n)

    class Meta:
        model = 'home.ServicePromise'


class ServiceNetFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: 'name-{0}'.format(n))
    linkman = factory.Sequence(lambda n: 'linkman-{0}'.format(n))
    mobile = factory.Sequence(lambda n: n)
    email = factory.Sequence(lambda n: '{}@h.com'.format(n))
    address = factory.Sequence(lambda n: 'address-{}'.format(n))

    class Meta:
        model = 'home.ServiceNet'


class FeedBackFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: 'name-{0}'.format(n))
    mobile = factory.Sequence(lambda n: '12345678')
    email = factory.Sequence(lambda n: '{}@h.com'.format(n))
    content = factory.Sequence(lambda n: 'content-{}'.format(n))

    class Meta:
        model = 'home.FeedBack'


class AboutUsFactory(factory.django.DjangoModelFactory):
    introduction = factory.Sequence(lambda n: 'introduction-{0}'.format(n))
    culture = factory.Sequence(lambda n: 'culture-{0}'.format(n))
    honour = factory.Sequence(lambda n: 'honour-{0}'.format(n))
    cooperativePartner = factory.Sequence(
        lambda n: 'cooperativePartner-{0}'.format(n))

    class Meta:
        model = 'home.AboutUs'


class FAQsFactory(factory.django.DjangoModelFactory):
    questioin = factory.Sequence(lambda n: 'questioin-{0}'.format(n))
    answer = factory.Sequence(lambda n: 'answer-{0}'.format(n))

    class Meta:
        model = 'home.FAQs'
