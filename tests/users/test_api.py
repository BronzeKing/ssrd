from tests import TestCase, factories


class UserTestCase(TestCase):
    def setUp(self):
        super(UserTestCase, self).setUp()
        self.baseurl = "/users"
        self.factory = factories.UserFactory
        self.obj = self.factory()

    def test_list(self):
        self.assertList(1)

    def test_create(self):
        self.data = {"email": "email@a.com", "username": "create", "password": "123456"}
        self.asserter().assertResource()

    def test_update(self):
        self.data = {"username": "update"}
        self.setBaseUrl(self.obj.id).asserter().assertResource()

    def test_retrieve(self):
        self.setBaseUrl(self.obj.id).asserter().assertResource()

    def test_delete(self):
        self.setBaseUrl(self.obj.id).asserter().assertResource()


class ProjectTestCase(TestCase):
    def setUp(self):
        super(ProjectTestCase, self).setUp()
        self.baseurl = "/projects"
        self.factory = factories.ProjectFactory
        self.obj = self.factory()

    def test_list(self):
        self.assertList()
        self.data = {"status": "0"}
        self.obj.status = 0
        self.obj.save()
        self.assertList()

    def test_create(self):
        self.data = {"name": "create", "type": "create", "linkman": "test", "budget": 1000, "duration": 100}
        self.asserter().assertResource()

    def test_update(self):
        self.data = {"name": "update"}
        self.setBaseUrl(self.obj.id).asserter().assertResource()

    def test_update_status(self):
        self.data = {"status": 0}
        self.setBaseUrl(self.obj.id).asserter().assertResource()

    def test_retrieve(self):
        self.setBaseUrl(self.obj.id).asserter().assertResource()

    def test_delete(self):
        self.setBaseUrl(self.obj.id).asserter().assertResource()


# class AuthorizeCodeTestCase(TestCase):
# def setUp(self):
# super(AuthorizeCodeTestCase, self).setUp()
# self.baseurl = "/authorizecodes"
# self.factory = factories.AuthorizeCodeFactory
# self.obj = self.factory()

# def test_list(self):
# self.assertList()

# def test_create(self):
# self.asserter().assertResource()

# def test_update(self):
# self.data = {"status": 0}
# self.setBaseUrl(self.obj.id).asserter().assertResource()

# def test_retrieve(self):
# self.setBaseUrl(self.obj.id).asserter().assertResource()

# def test_delete(self):
# self.setBaseUrl(self.obj.id).asserter().assertResource()


class CollectTestCase(TestCase):
    def setUp(self):
        super(CollectTestCase, self).setUp()
        self.baseurl = "/collects"
        self.factory = factories.CollectFactory
        self.obj = self.factory()

    def test_list(self):
        self.assertList()

    def test_create(self):
        self.data = {"productId": self.obj.product.id}
        self.asserter().assertResource()

    def test_delete(self):
        self.setBaseUrl(self.obj.id).asserter().assertResource()


class InvitationTestCase(TestCase):
    def setUp(self):
        super(InvitationTestCase, self).setUp()
        self.baseurl = "/invitations"
        self.factory = factories.InvitationFactory
        self.obj = self.factory()

    def test_list(self):
        self.assertList()


class MessagesTestCase(TestCase):
    def setUp(self):
        super(MessagesTestCase, self).setUp()
        self.baseurl = "/messages"
        self.factory = factories.MessageFactory
        self.obj = self.factory(userId=self.user.id)

    def test_list(self):
        self.assertList()

    def test_create(self):
        self.data = {"title": "title", "content": "content", "userId": self.user.id}
        self.asserter().assertResource()

    def test_delete(self):
        self.setBaseUrl(self.obj.id).asserter().assertResource()
