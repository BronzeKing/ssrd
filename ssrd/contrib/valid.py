import re
from ssrd.users import models as users
from ssrd.home import models as home
from ssrd import const
from paraer import Valid as _Valid, MethodProxy

__all__ = ("V")
ROLES = dict(const.ROLES)
STATUS = dict(const.STATUS)
ORDER_STATUS = dict(const.ORDER_STATUS)


class Valid(_Valid):
    def message(self, pk):
        self.msg = u'消息不存在'
        return users.Message.objects.get(pk=pk)

    def news(self, pk):
        self.msg = u'新闻公告不存在'
        return home.News.objects.get(pk=pk)

    def system(self, pk):
        self.msg = u'系统介绍不存在'
        return home.System.objects.get(pk=pk)

    def industryLink(self, pk):
        self.msg = u'行业介绍不存在'
        return home.IndustryLink.objects.get(pk=pk)

    def recruitmentCategory(self, pk):
        self.msg = u'招贤纳士类别不存在'
        return home.RecruitmentCategory.objects.get(pk=pk)

    def recruitment(self, pk):
        self.msg = u'招贤纳士不存在'
        return home.Recruitment.objects.get(pk=pk)

    def productCategory(self, pk):
        self.msg = u'产品类别不存在'
        return home.ProductCategory.objects.get(pk=pk)

    def aboutus(self, pk):
        self.msg = u'关于我们不存在'
        return home.AboutUs.objects.get(pk=pk)

    def faqs(self, pk):
        self.msg = u'FAQ不存在'
        return home.FAQs.objects.get(pk=pk)

    def feedback(self, pk):
        self.msg = u'反馈不存在'
        return home.FeedBack.objects.get(pk=pk)

    def servicenet(self, pk):
        self.msg = u'服务网点不存在'
        return home.ServiceNet.objects.get(pk=pk)

    def servicePromise(self, pk):
        self.msg = u'服务承诺不存在'
        return home.ServicePromise.objects.get(pk=pk)

    def product(self, pk):
        self.msg = u'产品不存在'
        return home.Product.objects.get(pk=pk)

    def consultationArticles(self, pk):
        self.msg = u'咨询我们不存在'
        return home.ConsultationArticles.objects.get(pk=pk)

    def charityActivity(self, pk):
        self.msg = u'公益活动不存在'
        return home.CharityActivity.objects.get(pk=pk)

    def user(self, pk):
        self.msg = u"用户不存在或已停用"
        user = users.User.objects.get(id=pk)
        return user

    def authorizecode(self, pk):
        self.msg = u"用户不存在或已停用"
        obj = users.AuthorizeCode.objects.get(pk=pk)
        return obj

    def invitation(self, pk):
        self.msg = u"用户不存在或已停用"
        obj = users.Invitation.objects.get(pk=pk)
        return obj

    def project(self, pk):
        self.msg = '项目不存在'
        obj = users.Project.objects.get(pk=pk)
        return obj

    def collect(self, pk):
        self.msg = "收藏品不存在"
        obj = users.Collect.objects.get(pk=pk)
        return obj

    def role(self, value):
        self.msg = "错误的参数值：%s" % str(ROLES)
        return int(value) in ROLES

    def status(self, value):
        self.msg = "错误的参数值：%s" % str(STATUS)
        return int(value) in STATUS

    def order_status(self, value):
        self.msg = "错误的参数值：%s" % str(ORDER_STATUS)
        return int(value) in ORDER_STATUS

    def name(self, name, length=200):
        if not name:
            self.msg = (u"此处不能留空")
        if len(name) > length:
            self.msg = (u"名称长度不能超过200")
            return
        if not const.RE_NAME.match(name):
            self.msg = (u"名称不能包含特殊字符")
            return
        return name.strip()

    def email(self, email):
        if const.RE_EMAIL.match(email):
            return email.strip()

    def username(self, username):
        if const.RE_NAME(username):
            return username.strip()

    def password(self, password):
        if len(password) < 6:
            self.msg = "密码长度不能小于6位"
            return
        return password

    def file(self, obj):
        if not hasattr(obj, 'file'):
            self.msg = '必须为文件类型'
        return obj

    def url(self, string):
        return string

    def num(self, num, n=1, bit=199, contain_0=True):
        self.msg = "必须为数值类型"
        if not num.isdigit():
            return
        return num


V = MethodProxy(Valid)
