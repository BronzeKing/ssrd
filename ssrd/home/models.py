from django.db import models
from django.utils.translation import ugettext_lazy as _


# Create your models here.
class RecruitmentCategory(models.Model):
    name = models.CharField("职位名称", max_length=50)
    created = models.DateTimeField("创建时间", auto_now_add=True)
    updated = models.DateTimeField("更新时间", auto_now=True)

    def __str__(self):
        return "<招贤纳士分类: {}".format(self.name)

    __repr__ = __str__

    def data(self):
        return dict(
            name=self.name,
            created=self.created,
            updated=self.updated,
            id=self.id)


class ProductCategory(models.Model):
    name = models.CharField("产品类别", max_length=50)
    created = models.DateTimeField("创建时间", auto_now_add=True)
    updated = models.DateTimeField("更新时间", auto_now=True)

    def __str__(self):
        return "<产品分类: {}".format(self.name)

    __repr__ = __str__

    def data(self):
        return dict(
            name=self.name,
            created=self.created,
            updated=self.updated,
            id=self.id)


class AboutUs(models.Model):
    introduction = models.TextField("简介")
    culture = models.TextField("企业文化")
    honour = models.TextField("荣耀")
    cooperativePartner = models.TextField("合作伙伴")

    def data(self):
        return dict(
            id=self.id,
            introduction=self.introduction,
            culture=self.culture,
            honour=self.honour,
            cooperativePartner=self.cooperativePartner)

    def __str__(self):
        return '关于我们'

    __repr__ = __str__


class FAQs(models.Model):
    questioin = models.TextField("问题")
    answer = models.TextField("回答")
    rank = models.IntegerField('排序', default=100)

    def __str__(self):
        return '<常见问答: ({}, {})>'.format(self.questioin, self.answer)

    def data(self):
        return dict(
            questioin=self.questioin,
            answer=self.answer,
            rank=self.rank,
            id=self.id)


class FeedBack(models.Model):
    """意见反馈"""
    name = models.CharField("姓名", max_length=50)
    mobile = models.IntegerField("手机号码", blank=True)
    email = models.EmailField("邮箱", blank=True)
    content = models.TextField("反馈内容")
    created = models.DateTimeField("创建时间", auto_now_add=True)

    def __str__(self):
        return '<意见反馈({}, {}, {}): {}>'.format(self.name, self.mobile,
                                               self.meail, self.content)

    __repr__ = __str__

    def data(self):
        return dict(
            id=sefl.id,
            name=self.name,
            mobile=self.mobile,
            email=self.email,
            content=self.content,
            created=self.created)


class ServiceNet(models.Model):
    name = models.CharField("网点名称", max_length=50)
    linkman = models.CharField("联系人", max_length=50)
    mobile = models.IntegerField("联系手机")
    email = models.EmailField(_('email address'))
    address = models.CharField("联系地址", max_length=100)
    rank = models.IntegerField('排序', default=100)

    def __str__(self):
        return '<(服务网点, ({}, {}, {}, {}, {})>'.format(
            self.name, self.linkman, self.mobile, self.email, self.address)

    __repr__ = __str__

    def data(self):
        return dict(
            id=self.id,
            name=self.name,
            linkman=self.linkman,
            mobile=self.mobile,
            email=self.email,
            address=self.address,
            rank=self.rank)


class ServicePromise(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    rank = models.IntegerField('排序', default=100)

    def __str__(self):
        return '<服务承诺: ({}, {})>'.format(self.title, self.content)

    __repr__ = __str__

    def data(self):
        return dict(
            title=self.title, content=self.content, rank=self.rank, id=self.id)


class Recruitment(models.Model):
    """招贤纳士"""
    name = models.CharField("职位名称", max_length=100)
    salary = models.CharField("薪资待遇", max_length=50)
    detail = models.TextField("职位简介")
    category = models.ForeignKey(
        RecruitmentCategory, verbose_name="职位类别", null=True)
    created = models.DateTimeField("创建时间", auto_now_add=True)
    updated = models.DateTimeField("更新时间", auto_now=True)

    def __str__(self):
        return '<招贤纳士: {}, {}>'.format(self.name, 'asdself.category.name')

    __repr__ = __str__

    def data(self):
        return dict(
            name=self.name,
            id=self.id,
            salary=self.salary,
            detail=self.detail,
            category=self.category.data(),
            created=self.created,
            updated=self.updated)


class Product(models.Model):
    name = models.CharField("产品名称", max_length=50)
    #  picture = models.ImageField("产品图片", upload_to=None)
    category = models.ForeignKey(
        ProductCategory, verbose_name="产品类别", null=True)
    created = models.DateTimeField("创建时间", auto_now_add=True)
    updated = models.DateTimeField("更新时间", auto_now=True)

    def __str__(self):
        return '<产品: {}, {}>'.format(self.name, 'self.category.name')

    __repr__ = __str__

    def data(self):
        return dict(
            name=self.name,
            id=self.id,
            #  picture=self.picture,
            category=self.category.data(),
            created=self.created,
            updated=self.updated)


class ConsultationArticles(models.Model):
    title = models.CharField("文章主题", max_length=200)
    content = models.TextField("文章内容")

    def __str__(self):
        return "<咨询我们: {}>".format(self.title)

    __repr__ = __str__

    def data(self):
        return dict(title=self.title, content=self.content, id=self.id)


class CharityActivity(models.Model):
    pass


class IndustryLink(models.Model):
    name = models.CharField("名称", max_length=255)
    picture = models.ImageField("背景图片", null=True)
    link = models.TextField("行业链接")
    rank = models.IntegerField("排序", default=100)

    def data(self):
        return dict(
            picture=self.picture.url,
            link=self.link,
            name=self.name,
            id=self.id)

    def __str__(self):
        return "<IndustryLink: {}, {}>".format(self.picture.url, self.link)

    __repr__ = __str__


class System(models.Model):
    name = models.CharField("名称", max_length=255)
    summary = models.TextField("简介摘要")
    introduction = models.TextField("系统介绍")
    feature = models.TextField("功能特性")
    structure = models.ImageField("系统结构", null=True)
    rank = models.IntegerField("排序", default=100)

    def data(self):
        return dict(
            name=self.name,
            id=self.id,
            summary=self.summary,
            introduction=self.introduction,
            feature=self.feature,
            structure=self.structure.url)

    def __str__(self):
        return "<System: {}, {}>".format(self.name, self.structure.url)

    __repr__ = __str__


class News(models.Model):
    title = models.TextField("标题")
    content = models.TextField("内容")
    created = models.DateTimeField("创建时间", auto_now_add=True)
    rank = models.IntegerField("排序", default=100)

    def data(self):
        return dict(
            id=self.id,
            title=self.title,
            content=self.content,
            created=self.created)

    def __str__(self):
        return "<News: {}, {}   {}>".format(self.title, self.content,
                                            self.created)

    __repr__ = __str__
