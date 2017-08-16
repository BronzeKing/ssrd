from ssrd.contrib import ViewSet, APIView, V
from ssrd.users.models import User, Group, Project
from ssrd.home.models import AboutUs, FAQs, FeedBack, ServiceNet, ServicePromise, Recruitment, Product
from paraer import para_ok_or_400

# Create your views here.


class AboutUsViewSet(ViewSet):
    serializer_class = AboutUs

    def list(self, request):
        """
        获取 关于我们
        """
        obj = AboutUs.objects.all()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400([{
        'name': 'id',
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
        'name': 'id',
        'method': V.aboutus,
        'description': '关于我们',
        'replace': 'obj'
    }])
    def destroy(self, request, obj=None, **kwargs):
        obj.delete()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400([{
        'name': 'id',
        'method': V.aboutus,
        'description': '关于我们',
        'replace': 'obj'
    }])
    def retrieve(self, request, obj=None, **kwargs):
        return self.result_class(data=obj)(serialize=True)


class FAQsViewSet(ViewSet):
    serializer_class = FAQs

    def list(self, request, **kwargs):
        """
        获取 FAQ
        """
        obj = FAQs.objects.all()
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
        'name': 'id',
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
        'name': 'id',
        'method': V.faqs,
        'description': 'FAQ',
        'replace': 'obj'
    }])
    def destroy(self, request, obj=None, **kwargs):
        obj.delete()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400([{
        'name': 'id',
        'method': V.faqs,
        'description': 'FAQ',
        'replace': 'obj'
    }])
    def retrieve(self, request, obj=None, **kwargs):
        return self.result_class(data=obj)(serialize=True)


class FeedBackViewSet(ViewSet):
    serializer_class = FeedBack

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
        'name': 'id',
        'method': V.feedback,
        'description': '意见反馈',
        'replace': 'obj'
    }, {
        'name': 'name',
        'description': '姓名'
    }, {
        'name': 'mobile',
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
        'name': 'id',
        'method': V.feedback,
        'description': '意见反馈',
        'replace': 'obj'
    }])
    def destroy(self, request, obj=None, **kwargs):
        obj.delete()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400([{
        'name': 'id',
        'method': V.feedback,
        'description': '意见反馈',
        'replace': 'obj'
    }])
    def retrieve(self, request, obj=None, **kwargs):
        return self.result_class(data=obj)(serialize=True)


class ServiceNetViewSet(ViewSet):
    serializer_class = ServiceNet

    def list(self, request, **kwargs):
        obj = ServiceNet.objects.all()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400([{
        'name': 'name',
        'description': '网点名称'
    }, {
        'name': 'mobile',
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
        'name': 'id',
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
        'name': 'id',
        'method': V.servicenet,
        'description': '服务网点',
        'replace': 'obj'
    }])
    def destroy(self, request, obj=None, **kwargs):
        obj.delete()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400([{
        'name': 'id',
        'method': V.servicenet,
        'description': '服务网点',
        'replace': 'obj'
    }])
    def retrieve(self, request, obj=None, **kwargs):
        return self.result_class(data=obj)(serialize=True)


class ServicePromiseViewSet(ViewSet):
    serializer_class = ServicePromise

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
        'name': 'id',
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
        'name': 'id',
        'method': V.servicePromise,
        'description': '服务承诺',
        'replace': 'obj'
    }])
    def destroy(self, request, obj=None, **kwargs):
        obj.delete()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400([{
        'name': 'id',
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
    serializer_class = Recruitment

    def list(self, request, **kwargs):
        """获取招贤纳士"""
        obj = Recruitment.objects.all()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400([{
        'name': 'name',
        'description': '职位名称',
        'method': V.name,
    }, {
        'name': 'salary',
        'description': '薪资待遇',
        'method': V.name,
    }, {
        'name': 'jobDetail',
        'description': '职位简介'
    }, {
        'name': 'category',
        'description': '职位类别',
        'method': V.recruitmentCategory
    }])
    def create(self, request, **kwargs):
        obj = Recruitment(**kwargs)
        obj.save()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400([{
        'name': 'id',
        'method': V.recruitment,
        'description': '招贤纳士',
        'replace': 'obj'
    }, {
        'name': 'name',
        'description': '职位名称',
        'method': V.name,
    }, {
        'name': 'salary',
        'description': '薪资待遇',
        'method': V.name,
    }, {
        'name': 'jobDetail',
        'description': '职位简介'
    }, {
        'name': 'category',
        'description': '职位类别',
        'method': V.recruitmentCategory
    }])
    def update(self, request, obj=None, **kwargs):
        [setattr(obj, k, v) for k, v in kwargs.items() if v]
        obj.save()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400([{
        'name': 'id',
        'method': V.recruitment,
        'description': '招贤纳士',
        'replace': 'obj'
    }])
    def destroy(self, request, obj=None, **kwargs):
        obj.delete()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400([{
        'name': 'id',
        'method': V.recruitment,
        'description': '招贤纳士',
        'replace': 'obj'
    }])
    def retrieve(self, request, obj=None, **kwargs):
        return self.result_class(data=obj)(serialize=True)


class ProductViewSet(ViewSet):
    serializer_class = Product
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
    }])
    def create(self, request, **kwargs):
        obj = Product(**kwargs)
        obj.save()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400([{
        'name': 'id',
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
        'method': V.recruitmentCategory
    }])
    def update(self, request, obj=None, **kwargs):
        [setattr(obj, k, v) for k, v in kwargs.items() if v]
        obj.save()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400([{
        'name': 'id',
        'description': '产品',
        'method': V.product,
        'replace': 'obj'
    }])
    def destroy(self, request, obj=None, **kwargs):
        obj.delete()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400([{
        'name': 'id',
        'description': '产品',
        'method': V.product,
        'replace': 'obj'
    }])
    def retrieve(self, request, obj=None, **kwargs):
        return self.result_class(data=obj)(serialize=True)
