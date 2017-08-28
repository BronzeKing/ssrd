import re
import json
from ssrd.users.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token

re_path = re.compile('{(\w+)}')


def methodbyfunc(funcname):
    """如果测试用例名称中含create或update,则调用对应的方法"""
    if 'create' in funcname:
        return 'post'
    if 'post' in funcname:
        return 'post'
    if 'update' in funcname:
        return 'put'
    if 'delete' in funcname:
        return 'delete'
    return 'get'


def get_reason(response):
    if response.status_code == 404:
        return '404!!!'
    if response.status_code == 500:
        return '500!!!'
    if response.status_code == 302:
        return '302!!!'
    if hasattr(response, 'data'):
        if response.status_code == 405:
            reason = response.data['detail']
            print(reason)
            return reason
        return str(response.data)
    return response.content


class TestCase(APITestCase):

    def setUp(self):
        self.user, ok = User.objects.get_or_create(
            username='root', email='root@h.com', password='123456', role=0)
        token, ok = Token.objects.get_or_create(user=self.user)
        # cls.c.put = partial(cls.c.put, content_type='application/json')
        # cls.c.patch = partial(cls.c.patch, content_type='application/json')
        self.data = {}
        self.baseurl = ''
        self.token = 'Token ' + token.key
        self.c = APIClient(HTTP_AUTHORIZATION=self.token)
        self.c.credentials(HTTP_AUTHORIZATION=self.token)
        self.c.force_authenticate(user=self.user)

    def asserter(self, status=200):
        method = self.data.pop(
            'method', None) or methodbyfunc(self._testMethodName) or 'get'
        url = getattr(self, 'url', self.baseurl)
        paths = re_path.findall(url)
        pathmap = {x: getattr(self.obj, x) for x in paths}
        if pathmap:
            url = url.format(**pathmap)
        data = self.data
        # data = method in ('put',
        # 'patch') and json.dumps(self.data) or self.data
        self.response = getattr(self.c, method)(url, data=data)
        self.assertEqual(self.response.status_code, status,
                         get_reason(self.response))
        return self

    def assertResource(self, attrset=['id', 'name']):
        resource = self.response.data
        for attr in attrset:
            left, right = self.data.get(attr), resource.get(attr)
            left and self.assertEqual(left, right,
                                      '%s is not equal by (%s, %s)' %
                                      (attr, left, right))
        return self

    def assertList(self, num=1):
        self.asserter().assertEqual(len(self.response.data.get('Records', [])), num)
        return self

    def setBaseUrl(self, pk):
        self.baseurl += '/{}'.format(pk)
        return self
