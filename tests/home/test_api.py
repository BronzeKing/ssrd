from tests import factories, TestCase


class AboutUsTestCase(TestCase):
    def setUp(self):
        super(AboutUsTestCase, self).setUp()
        self.baseurl = '/aboutus'
        self.factory = factories.AboutUsFactory
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
        self.factory = factories.FAQsFactory
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
        self.factory = factories.FeedBackFactory
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
        self.factory = factories.ServiceNetFactory
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
        self.factory = factories.ServicePromiseFactory
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
        self.factory = factories.RecruitmentFactory
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
            'salary': 'salary',
            'jobDetail': 'jobDetail',
            'address': 'address',
            'number': 3
            #  'category': self.obj.category.id
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
        self.factory = factories.ProductFactory
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


class NewsTestCase(TestCase):
    def setUp(self):
        super(NewsTestCase, self).setUp()
        self.baseurl = '/news'
        self.factory = factories.NewsFactory
        self.obj = self.factory()

    def test_list(self):
        self.assertList()

    def test_delete(self):
        self.setBaseUrl(self.obj.id).asserter().assertResource()

    def test_retrieve(self):
        self.setBaseUrl(self.obj.id).asserter().assertResource()

    def test_create(self):
        self.data = {'title': 'title', 'content': 'content'}
        self.asserter().assertResource()

    def test_update(self):
        self.data = {
            'title': 'test',
        }
        self.setBaseUrl(self.obj.id).asserter().assertResource()


class SystemTestCase(TestCase):
    def setUp(self):
        super(SystemTestCase, self).setUp()
        self.baseurl = '/systems'
        self.factory = factories.SystemFactory
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
            'summary': 'summary',
            'introduction': 'introduction',
            ' feature': 'feature',
            'structure': factories.FileFactory()
        }
        self.asserter().assertResource()

    def test_update(self):
        self.data = {
            'title': 'test',
        }
        self.setBaseUrl(self.obj.id).asserter().assertResource()


class IndustryLinkTestCase(TestCase):
    def setUp(self):
        super(IndustryLinkTestCase, self).setUp()
        self.baseurl = '/industryLinks'
        self.factory = factories.IndustryLinkFactory
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
            'link': 'www.test.com',
            'picture': factories.FileFactory()
        }
        self.asserter().assertResource()

    def test_update(self):
        self.data = {
            'name': 'test',
        }
        self.setBaseUrl(self.obj.id).asserter().assertResource()


class JobTestCase(TestCase):
    def setUp(self):
        super(JobTestCase, self).setUp()
        self.baseurl = '/jobs'
        self.factory = factories.JobFactory
        self.obj = self.factory()

    def test_create(self):
        self.data = {
            'name': '张三',
            'job': '项目工程师',
            'mobile': 1234567,
            'email': 'test@root.h',
            'attatchment': factories.FileFactory()
        }
        self.asserter().assertResource()


class DocumentTestCase(TestCase):
    def setUp(self):
        super(DocumentTestCase, self).setUp()
        self.baseurl = '/documents'
        self.factory = factories.DocumentFactory
        self.obj = self.factory()

    def test_create(self):
        self.data = {
            'name': 'document',
            'source': '0',
            'file': factories.FileFactory()
        }
        self.asserter().assertResource()

    def test_list(self):
        self.data = dict(source=1)
        self.assertList()

    def test_delete(self):
        self.setBaseUrl(self.obj.id).asserter().assertResource()

    def test_retrieve(self):
        self.setBaseUrl(self.obj.id).asserter().assertResource()

    def test_update(self):
        self.data = {
            'name': 'document',
            'source': '0',
            'file': factories.FileFactory()
        }
        self.setBaseUrl(self.obj.id).asserter().assertResource()
