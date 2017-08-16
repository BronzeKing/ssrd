from ssrd.contrib import TestCase
from ssrd.home.tests.factories import CharityActivityFactory, ConsultationArticlesFactory, ProductFactory, RecruitmentFactory, ServicePromiseFactory, ServiceNetFactory, FeedBackFactory, AboutUsFactory, FAQsFactory


class AboutUsTestCase(TestCase):
    def setUp(self):
        super(AboutUsTestCase, self).setUp()
        self.baseurl = '/aboutus'
        self.factory = AboutUsFactory
        self.obj = self.factory()

    def test_list(self):
        self.assertList()

    def test_delete(self):
        self.setBaseUrl(self.obj.id).asserter().assertResource()

    def test_retrieve(self):
        self.setBaseUrl(self.obj.id).asserter().assertResource()

    def test_create(self):
        self.data = {
            'introduction': 'create',
            'culture': 'culture',
            'honour': 'honour',
            'cooperativePartner': 'cooperativePartner'
        }
        self.asserter().assertResource()

    def test_update(self):
        self.data = {
            'introduction': 'update',
            'culture': 'culture',
            'honour': 'honour',
            'cooperativePartner': 'cooperativePartner'
        }
        self.setBaseUrl(self.obj.id).asserter().assertResource()


class FAQsTestCase(TestCase):
    def setUp(self):
        super(FAQsTestCase, self).setUp()
        self.baseurl = '/faqs'
        self.factory = FAQsFactory
        self.obj = self.factory()

    def test_list(self):
        self.assertList()

    def test_delete(self):
        self.setBaseUrl(self.obj.id).asserter().assertResource()

    def test_retrieve(self):
        self.setBaseUrl(self.obj.id).asserter().assertResource()

    def test_create(self):
        self.data = {'questioin': 'questioin', 'answer': 'answer'}
        self.asserter().assertResource()

    def test_update(self):
        self.data = {'questioin': 'questioin', 'answer': 'answer'}
        self.setBaseUrl(self.obj.id).asserter().assertResource()


class FeedBackTestCase(TestCase):
    def setUp(self):
        super(FeedBackTestCase, self).setUp()
        self.baseurl = '/feedBacks'
        self.factory = FeedBackFactory
        self.obj = self.factory()

    def test_list(self):
        self.assertList()

    def test_delete(self):
        self.setBaseUrl(self.obj.id).asserter().assertResource()

    def test_retrieve(self):
        self.setBaseUrl(self.obj.id).asserter().assertResource()

    def test_create(self):
        self.data = {
            'name': 'create',
            'mobile': '123455',
            'email': 'asd@h.com',
            'content': 'content'
        }
        self.asserter().assertResource()

    def test_update(self):
        self.data = {
            'name': 'create',
            'mobile': '123455',
            'email': 'asd@h.com',
            'content': 'content'
        }
        self.setBaseUrl(self.obj.id).asserter().assertResource()


class ServiceNetTestCase(TestCase):
    def setUp(self):
        super(ServiceNetTestCase, self).setUp()
        self.baseurl = '/serviceNets'
        self.factory = ServiceNetFactory
        self.obj = self.factory()

    def test_list(self):
        self.assertList()

    def test_delete(self):
        self.setBaseUrl(self.obj.id).asserter().assertResource()

    def test_retrieve(self):
        self.setBaseUrl(self.obj.id).asserter().assertResource()

    def test_create(self):
        self.data = {
            'name': 'create',
            'mobile': '123455',
            'email': 'asd@h.com',
            'linkman': 'linkman',
            'address': 'address'
        }
        self.asserter().assertResource()

    def test_update(self):
        self.data = {
            'name': 'create',
            'mobile': '123455',
            'email': 'asd@h.com',
            'linkman': 'linkman',
            'address': 'address'
        }
        self.setBaseUrl(self.obj.id).asserter().assertResource()


class ServicePromiseTestCase(TestCase):
    def setUp(self):
        super(ServicePromiseTestCase, self).setUp()
        self.baseurl = '/servicePromises'
        self.factory = ServicePromiseFactory
        self.obj = self.factory()

    def test_list(self):
        self.assertList()

    def test_delete(self):
        self.setBaseUrl(self.obj.id).asserter().assertResource()

    def test_retrieve(self):
        self.setBaseUrl(self.obj.id).asserter().assertResource()

    def test_create(self):
        self.data = {
            'title': 'title',
            'content': 'content',
        }
        self.asserter().assertResource()

    def test_update(self):
        self.data = {
            'title': 'title',
            'content': 'content',
        }
        self.setBaseUrl(self.obj.id).asserter().assertResource()


class RecruitmentTestCase(TestCase):
    def setUp(self):
        super(RecruitmentTestCase, self).setUp()
        self.baseurl = '/recruitments'
        self.factory = RecruitmentFactory
        self.obj = self.factory()

    def test_list(self):
        self.assertList()

    def test_delete(self):
        self.setBaseUrl(self.obj.id).asserter().assertResource()

    def test_retrieve(self):
        self.setBaseUrl(self.obj.id).asserter().assertResource()

    def test_create(self):
        self.data = {
            'title': 'title',
            'content': 'content',
            'category': self.obj.category.id
        }
        self.asserter().assertResource()

    def test_update(self):
        self.data = {
            'name': 'name',
            'salary': 'salary',
            'jobDetail': 'jobDetail',
        }
        self.setBaseUrl(self.obj.id).asserter().assertResource()


class ProductTestCase(TestCase):
    def setUp(self):
        super(ProductTestCase, self).setUp()
        self.baseurl = '/products'
        self.factory = ProductFactory
        self.obj = self.factory()

    def test_list(self):
        self.assertList()

    def test_delete(self):
        self.setBaseUrl(self.obj.id).asserter().assertResource()

    def test_retrieve(self):
        self.setBaseUrl(self.obj.id).asserter().assertResource()

    def test_create(self):
        self.data = {
            'name': 'name',
            'category': self.obj.category.id,
        }
        self.asserter().assertResource()

    def test_update(self):
        self.data = {
            'name': 'name',
            'category': self.obj.category.id,
        }
        self.setBaseUrl(self.obj.id).asserter().assertResource()
