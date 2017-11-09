from django.db import models
from django.utils.translation import ugettext_lazy as _

from ssrd import const


class Images(models.Model):
    image = models.ImageField("图片")


class RecruitmentCategory(models.Model):
    name = models.CharField("职位名称", max_length=50)
    created = models.DateTimeField("创建时间", auto_now_add=True)
    updated = models.DateTimeField("更新时间", auto_now=True)

    def __str__(self):
        return "<招贤纳士分类: {}".format(self.name)

    __repr__ = __str__


class ProductCategory(models.Model):
    name = models.CharField("产品类别", max_length=50)
    created = models.DateTimeField("创建时间", auto_now_add=True)
    updated = models.DateTimeField("更新时间", auto_now=True)

    def __str__(self):
        return "<产品分类: {}".format(self.name)

    __repr__ = __str__


class AboutUs(models.Model):
    introduction = models.TextField("简介")
    culture = models.TextField("企业文化")
    honour = models.TextField("荣耀")
    cooperativePartner = models.TextField("合作伙伴")

    def __str__(self):
        return '关于我们'

    __repr__ = __str__


class FAQs(models.Model):
    questioin = models.TextField("问题", db_index=True)
    answer = models.TextField("回答")
    rank = models.IntegerField('排序', default=100)
    created = models.DateTimeField("创建时间", auto_now_add=True)

    def __str__(self):
        return '<常见问答: ({}, {})>'.format(self.questioin, self.answer)


class FeedBack(models.Model):
    """意见反馈"""
    name = models.CharField("姓名", max_length=50)
    mobile = models.CharField("手机号码", blank=True, max_length=11)
    email = models.EmailField("邮箱", blank=True)
    content = models.TextField("反馈内容")
    created = models.DateTimeField("创建时间", auto_now_add=True)

    def __str__(self):
        return '<意见反馈({}, {}, {}): {}>'.format(self.name, self.mobile,
                                               self.meail, self.content)

    __repr__ = __str__


class ServiceNet(models.Model):
    name = models.CharField("网点名称", max_length=50)
    linkman = models.CharField("联系人", max_length=50)
    mobile = models.CharField("联系手机", max_length=11)
    email = models.EmailField(_('email address'))
    address = models.CharField("联系地址", max_length=100)
    rank = models.IntegerField('排序', default=100)

    def __str__(self):
        return '<(服务网点, ({}, {}, {}, {}, {})>'.format(
            self.name, self.linkman, self.mobile, self.email, self.address)

    __repr__ = __str__


class ServicePromise(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    rank = models.IntegerField('排序', default=100)

    def __str__(self):
        return '<服务承诺: ({}, {})>'.format(self.title, self.content)

    __repr__ = __str__


class Recruitment(models.Model):
    """招贤纳士"""
    name = models.CharField("职位名称", max_length=100, db_index=True)
    salary = models.CharField("薪资待遇", max_length=50)
    jobDetail = models.TextField("职位简介")
    jobResponsibilities = models.TextField("岗位职责")
    address = models.CharField("地点", max_length=100, default='')
    number = models.CharField("招聘数量", max_length=20, default='1')
    # category = models.ForeignKey(
    # RecruitmentCategory, verbose_name="职位类别")
    created = models.DateTimeField("创建时间", auto_now_add=True)
    updated = models.DateTimeField("更新时间", auto_now=True)

    def __str__(self):
        return '<招贤纳士: {}>'.format(self.name)

    __repr__ = __str__


class Product(models.Model):
    name = models.CharField("产品名称", max_length=50, db_index=True)
    description = models.TextField("产品描述")
    summary = models.TextField("产品概述")
    techParameter = models.TextField("技术参数")
    techParameter = models.TextField("技术参数")
    domain = models.TextField("应用领域")
    pictures = models.ManyToManyField("home.Images", verbose_name="产品插图")
    other = models.TextField("其他")
    background = models.ImageField("背景图片")
    category = models.ForeignKey(ProductCategory, verbose_name="产品分类")
    created = models.DateTimeField("创建时间", auto_now_add=True)
    updated = models.DateTimeField("更新时间", auto_now=True)

    def __str__(self):
        return '<产品: {}, {}>'.format(self.name, 'self.category.name')

    __repr__ = __str__


class ConsultationArticles(models.Model):
    title = models.CharField("文章主题", max_length=200)
    content = models.TextField("文章内容")

    def __str__(self):
        return "<咨询我们: {}>".format(self.title)

    __repr__ = __str__


class CharityActivity(models.Model):
    pass


class IndustryLink(models.Model):
    name = models.CharField("名称", max_length=255)
    picture = models.ImageField("背景图片", null=True)
    link = models.TextField("行业链接")
    rank = models.IntegerField("排序", default=100)

    def __str__(self):
        return "<IndustryLink: {}, {}>".format(self.picture.url, self.link)

    __repr__ = __str__


class System(models.Model):
    name = models.CharField("名称", max_length=255)
    summary = models.TextField("简介摘要")
    picture = models.ImageField("简介摘要插图")
    introduction = models.TextField("系统介绍")
    pictures = models.ManyToManyField("home.Images", verbose_name="系统插图")
    systemFeature = models.TextField("系统特性")
    structure = models.ImageField("系统结构", null=True)
    funtionalFeature = models.TextField("功能特性")
    rank = models.IntegerField("排序", default=100)

    def __str__(self):
        return "<System: {}, {}>".format(self.name, self.structure.url)

    __repr__ = __str__


class News(models.Model):
    title = models.TextField("标题")
    content = models.TextField("内容")
    created = models.DateTimeField("创建时间", auto_now_add=True)
    type = models.SmallIntegerField("类型", choices=const.NEWS, default=1)
    rank = models.IntegerField("排序", default=100)

    def __str__(self):
        return "<News: {}, {}   {}>".format(self.title, self.content,
                                            self.created)

    __repr__ = __str__


class Job(models.Model):
    name = models.CharField("姓名", max_length=100)
    job = models.TextField("职位", max_length=100)
    mobile = models.CharField("手机号码", blank=True, max_length=11)
    email = models.CharField("邮箱", max_length=100)
    attatchment = models.FileField("附件")
    updated = models.DateTimeField("更新时间", auto_now=True)

    def __str__(self):
        return "<job: {}   {}>".format(self.name, self.job)

    __repr__ = __str__


class Documents(models.Model):
    name = models.CharField("姓名", max_length=100, db_index=True)
    source = models.SmallIntegerField("来源", choices=const.SOURCES)
    file = models.FileField("文件", max_length=100)
    updated = models.DateTimeField("更新时间", auto_now=True)

    def __str__(self):
        return "<Documents: {}   {}>".format(self.name, self.source)

    __repr__ = __str__


class SystemCase(models.Model):
    """系统案例"""
    title = models.CharField("标题", max_length=255)
    summary = models.TextField("摘要")
    description = models.TextField("描述")
    address = models.CharField("工程地址", max_length=100)
    content = models.TextField("工程内容")
    picture = models.ImageField("背景图片")
    created = models.DateField("项目时间", default='2017-09-15')
    updated = models.DateTimeField("更新时间", auto_now=True)
    pictures = models.ManyToManyField("home.Images", verbose_name="系统案例插图")
    systems = models.ManyToManyField(
        "home.System", verbose_name="系统", related_name="systemCases")

    def __str__(self):
        return "<SystemCase: {}   {}>".format(self.title, self.summary)

    __repr__ = __str__
