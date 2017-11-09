from django.db.models import Q

from ssrd.contrib import ViewSet, V, send_mail, APIView
from ssrd.contrib.serializer import Serializer
from ssrd.home.models import AboutUs, FAQs, FeedBack, ServiceNet, ServicePromise, Recruitment, Product, IndustryLink, System, News
from ssrd.home import models as m
from ssrd import const
from paraer import para_ok_or_400

# Create your views here.


class AboutUsViewSet(ViewSet):
    serializer_class = Serializer(AboutUs)

    def list(self, request):
        """
        获取 关于我们
        """
        obj = AboutUs.objects.all()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400([{
        'name': 'pk',
        'method': V.aboutus,
        'description': '关于我们',
        'replace': 'obj',
    }, {
        'name': 'introduction',
        'description': '简介'
    }, {
        'name': 'culture',
        'description': '企业文化'
    }, {
        'name': 'honour',
        'description': '荣耀资质'
    }, {
        'name': 'cooperativePartner',
        'description': '合作伙伴'
    }])
    def update(self, request, obj=None, **kwargs):
        [setattr(obj, k, v) for k, v in kwargs.items() if v]
        obj.save()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400([{
        'name': 'introduction',
        'description': '简介'
    }, {
        'name': 'culture',
        'description': '企业文化'
    }, {
        'name': 'honour',
        'description': '荣耀资质'
    }, {
        'name': 'cooperativePartner',
        'description': '合作伙伴'
    }])
    def create(self, request, **kwargs):
        obj = AboutUs(**kwargs)
        obj.save()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400([{
        'name': 'pk',
        'method': V.aboutus,
        'description': '关于我们',
        'replace': 'obj'
    }])
    def destroy(self, request, obj=None, **kwargs):
        obj.delete()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400([{
        'name': 'pk',
        'method': V.aboutus,
        'description': '关于我们',
        'replace': 'obj'
    }])
    def retrieve(self, request, obj=None, **kwargs):
        return self.result_class(data=obj)(serialize=True)


class FAQsViewSet(ViewSet):
    serializer_class = Serializer(FAQs)

    @para_ok_or_400([{
        'name': 'search',
        'description': '搜索',
    }])
    def list(self, request, search=None, **kwargs):
        """
        获取 FAQ
        """
        obj = FAQs.objects.all()
        if search:
            obj = obj.filter(
                Q(questioin__contains=search) | Q(answer__contains=search))
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400([{
        'name': 'answer',
        'description': '回答'
    }, {
        'name': 'questioin',
        'description': '问题'
    }])
    def create(self, request, **kwargs):
        obj = FAQs(**kwargs)
        obj.save()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400([{
        'name': 'pk',
        'method': V.faqs,
        'description': 'FAQ',
        'replace': 'obj'
    }, {
        'name': 'answer',
        'description': '回答'
    }, {
        'name': 'questioin',
        'description': '问题'
    }])
    def update(self, request, obj=None, **kwargs):
        [setattr(obj, k, v) for k, v in kwargs.items() if v]
        obj.save()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400([{
        'name': 'pk',
        'method': V.faqs,
        'description': 'FAQ',
        'replace': 'obj'
    }])
    def destroy(self, request, obj=None, **kwargs):
        obj.delete()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400([{
        'name': 'pk',
        'method': V.faqs,
        'description': 'FAQ',
        'replace': 'obj',
    }])
    def retrieve(self, request, obj=None, **kwargs):
        return self.result_class(data=obj)(serialize=True)


class FeedBackViewSet(ViewSet):
    serializer_class = Serializer(FeedBack)

    def list(self, request, **kwargs):
        """
        获取意见反馈
        """
        obj = FeedBack.objects.all()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400([{
        'name': 'name',
        'description': '姓名'
    }, {
        'name': 'mobile',
        'methid': V.mobile,
        'description': '联系号码'
    }, {
        'name': 'email',
        'description': '联系邮箱'
    }, {
        'name': 'content',
        'description': '反馈内容'
    }])
    def create(self, request, **kwargs):
        obj = FeedBack(**kwargs)
        obj.save()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400([{
        'name': 'pk',
        'method': V.feedback,
        'description': '意见反馈',
        'replace': 'obj'
    }, {
        'name': 'name',
        'description': '姓名'
    }, {
        'name': 'mobile',
        'method': V.mobile,
        'description': '联系号码'
    }, {
        'name': 'email',
        'description': '联系邮箱'
    }, {
        'name': 'content',
        'description': '反馈内容'
    }])
    def update(self, request, obj=None, **kwargs):
        [setattr(obj, k, v) for k, v in kwargs.items() if v]
        obj.save()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400([{
        'name': 'pk',
        'method': V.feedback,
        'description': '意见反馈',
        'replace': 'obj'
    }])
    def destroy(self, request, obj=None, **kwargs):
        obj.delete()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400([{
        'name': 'pk',
        'method': V.feedback,
        'description': '意见反馈',
        'replace': 'obj'
    }])
    def retrieve(self, request, obj=None, **kwargs):
        return self.result_class(data=obj)(serialize=True)


class ServiceNetViewSet(ViewSet):
    serializer_class = Serializer(ServiceNet)

    def list(self, request, **kwargs):
        obj = ServiceNet.objects.all()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400([{
        'name': 'name',
        'description': '网点名称'
    }, {
        'name': 'mobile',
        'method': V.mobile,
        'description': '联系号码'
    }, {
        'name': 'linkmap',
        'description': '联系人'
    }, {
        'name': 'email',
        'description': '联系邮箱'
    }, {
        'name': 'address',
        'description': '联系地址'
    }])
    def create(self, request, **kwargs):
        obj = ServiceNet(**kwargs)
        obj.save()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400([{
        'name': 'pk',
        'method': V.servicenet,
        'description': '服务网点',
        'replace': 'obj'
    }, {
        'name': 'name',
        'description': '网点名称'
    }, {
        'name': 'linkmap',
        'description': '联系人'
    }, {
        'name': 'mobile',
        'method': V.mobile,
        'description': '联系号码'
    }, {
        'name': 'email',
        'description': '联系邮箱'
    }, {
        'name': 'address',
        'description': '联系地址'
    }])
    def update(self, request, obj=None, **kwargs):
        [setattr(obj, k, v) for k, v in kwargs.items() if v]
        obj.save()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400([{
        'name': 'pk',
        'method': V.servicenet,
        'description': '服务网点',
        'replace': 'obj'
    }])
    def destroy(self, request, obj=None, **kwargs):
        obj.delete()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400([{
        'name': 'pk',
        'method': V.servicenet,
        'description': '服务网点',
        'replace': 'obj'
    }])
    def retrieve(self, request, obj=None, **kwargs):
        return self.result_class(data=obj)(serialize=True)


class ServicePromiseViewSet(ViewSet):
    serializer_class = Serializer(ServicePromise)

    def list(self, request, **kwargs):
        """
        获取服务承诺列表
        """
        obj = ServicePromise.objects.all()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400([{
        'name': 'title',
        'description': '标题'
    }, {
        'name': 'content',
        'description': '内容'
    }])
    def create(self, request, **kwargs):
        obj = ServicePromise(**kwargs)
        obj.save()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400([{
        'name': 'pk',
        'method': V.servicePromise,
        'description': '服务承诺',
        'replace': 'obj'
    }, {
        'name': 'title',
        'description': '标题'
    }, {
        'name': 'content',
        'description': '内容'
    }])
    def update(self, request, obj=None, **kwargs):
        [setattr(obj, k, v) for k, v in kwargs.items() if v]
        obj.save()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400([{
        'name': 'pk',
        'method': V.servicePromise,
        'description': '服务承诺',
        'replace': 'obj'
    }])
    def destroy(self, request, obj=None, **kwargs):
        obj.delete()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400([{
        'name': 'pk',
        'method': V.servicePromise,
        'description': '服务承诺',
        'replace': 'obj'
    }])
    def retrieve(self, request, obj=None, **kwargs):
        return self.result_class(data=obj)(serialize=True)


class RecruitmentViewSet(ViewSet):
    """
    招贤纳士
    """
    serializer_class = Serializer(Recruitment)

    @para_ok_or_400([{
        'name': 'search',
        'description': '搜索',
    }])
    def list(self, request, search=None, **kwargs):
        """获取招贤纳士"""
        obj = Recruitment.objects.all()
        if search:
            obj = obj.filter(
                Q(name__contains=search) | Q(salary__contains=search) |
                Q(jobDetail__contains=search) |
                Q(jobResponsibilities__contains=search))
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400([
        {
            'name': 'name',
            'description': '职位名称',
        },
        {
            'name': 'salary',
            'description': '薪资待遇',
            'method': V.name,
        },
        {
            'name': 'jobDetail',
            'description': '职位简介'
        },
        {
            'name': 'address',
            'description': '职位地点'
        },
        {
            'name': 'number',
            'description': '职位数量',
            # }, {
            # 'name': 'category',
            # 'description': '职位类别',
            # 'method': V.recruitmentCategory
        }
    ])
    def create(self, request, **kwargs):
        obj = Recruitment(**kwargs)
        obj.save()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400([
        {
            'name': 'pk',
            'method': V.recruitment,
            'description': '招贤纳士',
            'replace': 'obj'
        },
        {
            'name': 'name',
            'description': '职位名称',
        },
        {
            'name': 'salary',
            'description': '薪资待遇',
            'method': V.name,
        },
        {
            'name': 'jobDetail',
            'description': '职位简介'
        },
        {
            'name': 'address',
            'description': '职位地点'
        },
        {
            'name': 'number',
            'description': '职位数量',
            # }, {
            # 'name': 'category',
            # 'description': '职位类别',
            # 'method': V.recruitmentCategory
        }
    ])
    def update(self, request, obj=None, **kwargs):
        [setattr(obj, k, v) for k, v in kwargs.items() if v]
        obj.save()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400([{
        'name': 'pk',
        'method': V.recruitment,
        'description': '招贤纳士',
        'replace': 'obj'
    }])
    def destroy(self, request, obj=None, **kwargs):
        obj.delete()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400([{
        'name': 'pk',
        'method': V.recruitment,
        'description': '招贤纳士',
        'replace': 'obj'
    }])
    def retrieve(self, request, obj=None, **kwargs):
        return self.result_class(data=obj)(serialize=True)


class ProductViewSet(ViewSet):
    serializer_class = Serializer(Product)
    """产品"""

    def list(self, request, **kwargs):
        """获取产品列表"""
        obj = Product.objects.all()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400([{
        'name': 'name',
        'description': '产品名称',
        'method': V.name,
    }, {
        'name': 'category',
        'description': '产品类别',
        'method': V.productCategory,
    }, {
        'name': 'picture',
        'description': '产品图片',
        'type': 'file'
    }])
    def create(self, request, **kwargs):
        obj = Product(**kwargs)
        obj.save()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400([{
        'name': 'pk',
        'description': '产品',
        'method': V.product,
        'replace': 'obj'
    }, {
        'name': 'name',
        'description': '产品名称',
        'method': V.name,
    }, {
        'name': 'category',
        'description': '产品类别',
        'method': V.productCategory,
    }, {
        'name': 'picture',
        'description': '产品图片',
        'type': 'file',
        'method': V.recruitmentCategory
    }])
    def update(self, request, obj=None, **kwargs):
        [setattr(obj, k, v) for k, v in kwargs.items() if v]
        obj.save()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400([{
        'name': 'pk',
        'description': '产品',
        'method': V.product,
        'replace': 'obj'
    }])
    def destroy(self, request, obj=None, **kwargs):
        obj.delete()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400([{
        'name': 'pk',
        'description': '产品',
        'method': V.product,
        'replace': 'obj'
    }])
    def retrieve(self, request, obj=None, **kwargs):
        return self.result_class(data=obj)(serialize=True)


class IndustryLinkViewSet(ViewSet):
    """
    行业链接
    """
    serializer_class = Serializer(IndustryLink)

    def list(self, request, **kwargs):
        """获取行业链接"""
        obj = IndustryLink.objects.all().order_by('rank')
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400([{
        'name': 'name',
        'description': '名称',
        'method': V.name,
    }, {
        'name': 'link',
        'description': '行业链接',
        'method': V.url,
    }, {
        'name': 'picture',
        'description': '背景图片',
        'method': V.file,
        'type': 'file'
    }])
    def create(self, request, **kwargs):
        obj = IndustryLink(**kwargs)
        obj.save()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400([{
        'name': 'pk',
        'description': '行业链接',
        'method': V.industryLink,
        'replace': 'obj'
    }, {
        'name': 'name',
        'description': '产品名称',
        'method': V.name,
    }, {
        'name': 'link',
        'description': '行业链接',
        'method': V.url,
    }, {
        'name': 'picture',
        'description': '背景图片',
        'method': V.file,
        'type': 'file'
    }])
    def update(self, request, obj=None, **kwargs):
        [setattr(obj, k, v) for k, v in kwargs.items() if v]
        obj.save()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400([{
        'name': 'pk',
        'description': '行业链接',
        'method': V.industryLink,
        'replace': 'obj'
    }])
    def destroy(self, request, obj=None, **kwargs):
        obj.delete()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400([{
        'name': 'pk',
        'description': '行业链接',
        'method': V.industryLink,
        'replace': 'obj'
    }])
    def retrieve(self, request, obj=None, **kwargs):
        return self.result_class(data=obj)(serialize=True)


class SystemViewSet(ViewSet):
    """
    系统展示
    """
    serializer_class = Serializer(System, extra=['pictures', 'systemCases'])

    def list(self, request, **kwargs):
        """获取系统展示"""
        obj = System.objects.all().order_by('rank')
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400([{
        'name': 'name',
        'description': '名称',
        'method': V.name,
    }, {
        'name': 'summary',
        'description': '简介摘要',
    }, {
        'name': 'summaryPicture',
        'description': '简介摘要插图',
        'method': V.file,
        'type': 'file'
    }, {
        'name': 'introduction',
        'description': '系统介绍',
    }, {
        'name': 'systemFeature',
        'description': '系统特性',
    }, {
        'name': 'structure',
        'description': '系统结构',
        'method': V.file,
        'type': 'file'
    }, {
        'name': 'funtionalFeature',
        'description': '功能特性',
    }, {
        'name': 'picture1',
        'description': '现场图片1',
        'method': V.file,
        'type': 'file'
    }, {
        'name': 'picture2',
        'description': '现场图片2',
        'method': V.file,
        'type': 'file'
    }, {
        'name': 'picture3',
        'description': '现场图片3',
        'method': V.file,
        'type': 'file'
    }])
    def create(self, request, **kwargs):
        obj = System(**kwargs)
        obj.save()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400([{
        'name': 'pk',
        'description': '系统',
        'method': V.system,
        'replace': 'obj'
    }, {
        'name': 'name',
        'description': '名称',
        'method': V.name,
    }, {
        'name': 'summary',
        'description': '简介摘要',
    }, {
        'name': 'summaryPicture',
        'description': '简介摘要插图',
        'method': V.file,
        'type': 'file'
    }, {
        'name': 'introduction',
        'description': '系统介绍',
    }, {
        'name': 'systemFeature',
        'description': '系统特性',
    }, {
        'name': 'structure',
        'description': '系统结构',
        'method': V.file,
        'type': 'file'
    }, {
        'name': 'funtionalFeature',
        'description': '功能特性',
    }, {
        'name': 'picture1',
        'description': '现场图片1',
        'method': V.file,
        'type': 'file'
    }, {
        'name': 'picture2',
        'description': '现场图片2',
        'method': V.file,
        'type': 'file'
    }, {
        'name': 'picture3',
        'description': '现场图片3',
        'method': V.file,
        'type': 'file'
    }])
    def update(self, request, obj=None, **kwargs):
        [setattr(obj, k, v) for k, v in kwargs.items() if v]
        obj.save()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400([{
        'name': 'pk',
        'description': '系统',
        'method': V.system,
        'replace': 'obj'
    }])
    def destroy(self, request, obj=None, **kwargs):
        obj.delete()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400([{
        'name': 'pk',
        'description': '系统',
        'method': V.system,
        'replace': 'obj'
    }])
    def retrieve(self, request, obj=None, **kwargs):
        return self.result_class(data=obj)(serialize=True)


class NewsViewSet(ViewSet):
    """
    最新公告
    """
    serializer_class = Serializer(News)

    @para_ok_or_400([{
        'name': 'search',
        'description': '搜索',
    }, {
        'name': 'type',
        'description': dict(const.NEWS, description='新闻类型'),
    }])
    def list(self, request, search=None, **kwargs):
        """获取新闻公告"""
        obj = News.objects.all().order_by('rank', 'created')
        if search:
            obj = obj.filter(
                Q(title__contains=search) | Q(content__contains=search))
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400([{
        'name': 'title',
        'description': '标题',
    }, {
        'name': 'content',
        'description': '内容',
    }])
    def create(self, request, **kwargs):
        """
        新建新闻公告
        """
        obj = News(**kwargs)
        obj.save()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400([{
        'name': 'pk',
        'description': '新闻公告',
        'method': V.news,
        'replace': 'obj'
    }, {
        'name': 'title',
        'description': '标题',
    }, {
        'name': 'content',
        'description': '内容',
    }])
    def update(self, request, obj=None, **kwargs):
        """
        修改单条新闻公告
        """
        [setattr(obj, k, v) for k, v in kwargs.items() if v]
        obj.save()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400([{
        'name': 'pk',
        'description': '新闻公告',
        'method': V.news,
        'replace': 'obj'
    }])
    def destroy(self, request, obj=None, **kwargs):
        """
        删除单条新闻公告
        """
        obj.delete()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400([{
        'name': 'pk',
        'description': '新闻公告',
        'method': V.news,
        'replace': 'obj'
    }])
    def retrieve(self, request, obj=None, **kwargs):
        """
        获取单条新闻公告
        """
        return self.result_class(data=obj)(serialize=True)


class JobViewSet(ViewSet):
    """
    职位申请
    """
    serializer_class = Serializer(m.Job)

    @para_ok_or_400([{
        'name': 'name',
        'description': '姓名',
        'method': V.name
    }, {
        'name': 'job',
        'description': '职位',
    }, {
        'name': 'mobile',
        'description': '电话',
        'method': V.mobile
    }, {
        'name': 'email',
        'description': '邮箱',
        'method': V.email
    }, {
        'name': 'attatchment',
        'description': '附件',
        'type': 'file',
        'method': V.file,
        'required': True
    }])
    def create(self,
               request,
               name=None,
               job=None,
               mobile=None,
               email=None,
               attatchment=None,
               **kwargs):
        """职位申请"""
        obj = m.Job(
            name=name,
            job=job,
            mobile=mobile,
            email=email,
            attatchment=attatchment)
        obj.save()
        subject = "求职简历"
        content = "职位申请：\n岗位：{}\n姓名：{}\n手机：{}\n邮箱：{}\n附件为\n{}".format(
            job, name, mobile, email, obj.attatchment.url)
        send_mail(subject, content, "ssrdhr@foxmail.com")
        send_mail(subject, content, "drinks.huang@hypers.com")
        return self.result_class(data=obj)(serialize=True)


class DocumentsViewSet(ViewSet):
    """
    文档
    """
    serializer_class = Serializer(m.Documents)

    @para_ok_or_400([{
        'name': 'source',
        'description': dict(const.SOURCES, description='来源'),
        'required': True
    }, {
        'name': 'search',
        'description': '搜索',
    }])
    def list(self, request, search=None, source=None, **kwargs):
        """获取文档列表"""
        obj = m.Documents.objects.all()
        if int(source) != -1:
            obj = obj.filter(source=source)
        if search:
            obj = obj.filter(Q(name__contains=search))
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400([{
        'name': 'name',
        'description': '名称',
    }, {
        'name': 'source',
        'description': dict(const.SOURCES, description='来源'),
    }, {
        'name': 'file',
        'description': '文件',
        'type': 'file',
        'method': V.file,
        'required': True
    }])
    def create(self, request, **kwargs):
        """新建文档"""
        obj = m.Documents(**kwargs)
        obj.save()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400([{
        'name': 'pk',
        'method': V.document,
        'description': '文档',
        'replace': 'obj'
    }, {
        'name': 'name',
        'description': '名称',
    }, {
        'name': 'source',
        'description': dict(const.SOURCES, description='来源'),
    }, {
        'name': 'file',
        'description': '文件',
        'type': 'file',
        'method': V.file,
        'required': True
    }])
    def update(self, request, obj, **kwargs):
        """更新文档"""
        [setattr(obj, k, v) for k, v in kwargs.items() if v]
        obj.save()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400([{
        'name': 'pk',
        'description': '文档',
        'method': V.document,
        'replace': 'obj'
    }])
    def destroy(self, request, obj=None, **kwargs):
        """
        删除单条文档
        """
        obj.delete()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400([{
        'name': 'pk',
        'description': '文档',
        'method': V.document,
        'replace': 'obj'
    }])
    def retrieve(self, request, obj=None, **kwargs):
        """
        获取文档
        """
        return self.result_class(data=obj)(serialize=True)


class SystemCaseViewSet(ViewSet):
    """
    文档
    """
    serializer_class = Serializer(m.SystemCase, extra=['pictures', 'systems'])

    def list(self, request, **kwargs):
        """获取案例展示"""
        obj = m.SystemCase.objects.all()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400([{
        'name': 'pk',
        'description': '文档',
        'method': V.systemCase,
        'replace': 'obj'
    }])
    def retrieve(self, request, obj=None, **kwargs):
        """
        获取文档
        """
        return self.result_class(data=obj)(serialize=True)


class ConstView(APIView):
    def get(self, request):
        """
        获取常量
        """
        data = {}
        for x in const.__all__:
            if not x.startswith('__'):
                try:
                    data[x] = dict(getattr(const, x))
                except:
                    pass
        return self.result_class(data=data)()


class EnvView(APIView):
    def get(self, request):
        """
        获取常量
        """
        domain = ('http://',
                  'https://')[request.is_secure()] + request.get_host()
        oauth = domain + '/login/{}/'
        oauth = [
            dict(name=x, url=oauth.format(x))
            for x in ('qq', 'weibo', 'weixin')
        ]

        document = dict(const.SOURCES)
        document = {y: x for x, y in document.items()}

        status = dict(const.STATUS)
        statusReverse = {y: x for x, y in status.items()}

        projectLog = {y: x for x, y in const.ProjectLog}
        data = dict(
            oauth=oauth,
            document=document,
            status=status,
            statusReverse=statusReverse,
            projectLog=projectLog)
        return self.result_class(data)()
