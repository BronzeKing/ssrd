from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from collections import defaultdict

from ssrd.contrib import ViewSet, V, send_mail, APIView
from ssrd.contrib.serializer import Serializer
from ssrd.home.models import (
    AboutUs,
    FAQs,
    FeedBack,
    ServiceNet,
    ServicePromise,
    Recruitment,
    Product,
    IndustryLink,
    System,
    News,
)
from ssrd.home import models as m
from ssrd import const
from paraer import para_ok_or_400

# Create your views here.


class AboutUsView(APIView):
    serializer_class = Serializer(m.AboutUs)

    @para_ok_or_400(
        [
            {
                "name": "pk",
                "method": V.aboutus,
                "description": "关于我们",
                "replace": "obj",
            },
            {"name": "introduction", "description": "简介"},
            {"name": "culture", "description": "企业文化"},
            {"name": "email", "description": "邮箱", "method": V.email},
            {"name": "address", "method": V.address, "description": "地址"},
            {"name": "tel", "method": lambda x: len(x) < 20, "description": "电话"},
            {"name": "postcode", "method": lambda x: len(x) < 10, "description": "邮编"},
        ]
    )
    def create(self, request, obj=None, **kwargs):
        [setattr(obj, k, v) for k, v in kwargs.items() if v]
        obj.save()
        return self.result_class(data=obj)(serialize=True)

    def get(self, request, **kwargs):
        obj, ok = m.AboutUs.objects.get_or_create()
        return self.result_class(data=obj)(serialize=True)


class FeedBackViewSet(ViewSet):
    serializer_class = Serializer(FeedBack)

    def list(self, request, **kwargs):
        """
        获取意见反馈
        """
        obj = FeedBack.objects.all()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400(
        [
            {"name": "name", "description": "姓名"},
            {"name": "mobile", "methid": V.mobile, "description": "联系号码"},
            {"name": "email", "description": "联系邮箱"},
            {"name": "content", "description": "反馈内容"},
        ]
    )
    def create(self, request, **kwargs):
        obj = FeedBack(**kwargs)
        obj.save()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400(
        [
            {
                "name": "pk",
                "method": V.feedback,
                "description": "意见反馈",
                "replace": "obj",
            },
            {"name": "name", "description": "姓名"},
            {"name": "mobile", "method": V.mobile, "description": "联系号码"},
            {"name": "email", "description": "联系邮箱"},
            {"name": "content", "description": "反馈内容"},
        ]
    )
    def update(self, request, obj=None, **kwargs):
        [setattr(obj, k, v) for k, v in kwargs.items() if v]
        obj.save()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400(
        [{"name": "pk", "method": V.feedback, "description": "意见反馈", "replace": "obj"}]
    )
    def destroy(self, request, obj=None, **kwargs):
        obj.delete()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400(
        [{"name": "pk", "method": V.feedback, "description": "意见反馈", "replace": "obj"}]
    )
    def retrieve(self, request, obj=None, **kwargs):
        return self.result_class(data=obj)(serialize=True)


class ServiceNetViewSet(ViewSet):
    serializer_class = Serializer(ServiceNet)

    def list(self, request, **kwargs):
        obj = ServiceNet.objects.all()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400(
        [
            {"name": "name", "description": "网点名称"},
            {"name": "mobile", "method": V.mobile, "description": "联系号码"},
            {"name": "linkmap", "description": "联系人"},
            {"name": "email", "description": "联系邮箱"},
            {"name": "address", "description": "联系地址"},
        ]
    )
    def create(self, request, **kwargs):
        obj = ServiceNet(**kwargs)
        obj.save()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400(
        [
            {
                "name": "pk",
                "method": V.servicenet,
                "description": "服务网点",
                "replace": "obj",
            },
            {"name": "name", "description": "网点名称"},
            {"name": "linkmap", "description": "联系人"},
            {"name": "mobile", "method": V.mobile, "description": "联系号码"},
            {"name": "email", "description": "联系邮箱"},
            {"name": "address", "description": "联系地址"},
        ]
    )
    def update(self, request, obj=None, **kwargs):
        [setattr(obj, k, v) for k, v in kwargs.items() if v]
        obj.save()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400(
        [
            {
                "name": "pk",
                "method": V.servicenet,
                "description": "服务网点",
                "replace": "obj",
            }
        ]
    )
    def destroy(self, request, obj=None, **kwargs):
        obj.delete()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400(
        [
            {
                "name": "pk",
                "method": V.servicenet,
                "description": "服务网点",
                "replace": "obj",
            }
        ]
    )
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

    @para_ok_or_400(
        [
            {"name": "title", "description": "标题"},
            {"name": "content", "description": "内容"},
        ]
    )
    def create(self, request, **kwargs):
        obj = ServicePromise(**kwargs)
        obj.save()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400(
        [
            {
                "name": "pk",
                "method": V.servicePromise,
                "description": "服务承诺",
                "replace": "obj",
            },
            {"name": "title", "description": "标题"},
            {"name": "content", "description": "内容"},
        ]
    )
    def update(self, request, obj=None, **kwargs):
        [setattr(obj, k, v) for k, v in kwargs.items() if v]
        obj.save()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400(
        [
            {
                "name": "pk",
                "method": V.servicePromise,
                "description": "服务承诺",
                "replace": "obj",
            }
        ]
    )
    def destroy(self, request, obj=None, **kwargs):
        obj.delete()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400(
        [
            {
                "name": "pk",
                "method": V.servicePromise,
                "description": "服务承诺",
                "replace": "obj",
            }
        ]
    )
    def retrieve(self, request, obj=None, **kwargs):
        return self.result_class(data=obj)(serialize=True)


class RecruitmentViewSet(ViewSet):
    """
    招贤纳士
    """

    serializer_class = Serializer(Recruitment)

    @para_ok_or_400([{"name": "search", "description": "搜索"}])
    def list(self, request, search=None, **kwargs):
        """获取招贤纳士"""
        obj = Recruitment.objects.all()
        if search:
            obj = obj.filter(
                Q(name__contains=search)
                | Q(salary__contains=search)
                | Q(jobDetail__contains=search)
                | Q(jobResponsibilities__contains=search)
            )
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400(
        [
            {"name": "name", "description": "职位名称"},
            {"name": "salary", "description": "薪资待遇", "method": V.name},
            {"name": "jobDetail", "description": "职位简介"},
            {"name": "address", "description": "职位地点"},
            {
                "name": "number",
                "description": "职位数量",
                # }, {
                # 'name': 'category',
                # 'description': '职位类别',
                # 'method': V.recruitmentCategory
            },
        ]
    )
    def create(self, request, **kwargs):
        obj = Recruitment(**kwargs)
        obj.save()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400(
        [
            {
                "name": "pk",
                "method": V.recruitment,
                "description": "招贤纳士",
                "replace": "obj",
            },
            {"name": "name", "description": "职位名称"},
            {"name": "salary", "description": "薪资待遇", "method": V.name},
            {"name": "jobDetail", "description": "职位简介"},
            {"name": "address", "description": "职位地点"},
            {
                "name": "number",
                "description": "职位数量",
                # }, {
                # 'name': 'category',
                # 'description': '职位类别',
                # 'method': V.recruitmentCategory
            },
        ]
    )
    def update(self, request, obj=None, **kwargs):
        [setattr(obj, k, v) for k, v in kwargs.items() if v]
        obj.save()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400(
        [
            {
                "name": "pk",
                "method": V.recruitment,
                "description": "招贤纳士",
                "replace": "obj",
            }
        ]
    )
    def destroy(self, request, obj=None, **kwargs):
        obj.delete()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400(
        [
            {
                "name": "pk",
                "method": V.recruitment,
                "description": "招贤纳士",
                "replace": "obj",
            }
        ]
    )
    def retrieve(self, request, obj=None, **kwargs):
        return self.result_class(data=obj)(serialize=True)


def categoryTree(obj, action, lower):
    data = dict(id=obj.id, name=obj.name)
    category_set = obj.category_set.all().prefetch_related("category_set")
    data["sub"] = [categoryTree(x, action, lower) for x in category_set]
    action == "low" and not data["sub"] and lower.append(data)
    return data


class CategoryViewSet(ViewSet):
    serializer_class = Serializer(m.Category, dep=5)

    @para_ok_or_400(
        [
            {"name": "search", "description": "搜索字段"},
            {"name": "action", "description": {"low": "返回最低级的目录", "top": "返回顶级目录"}},
        ]
    )
    def list(self, request, search=None, action=None, **kwargs):
        """获取产品目录列表"""
        obj = (
            m.Category.objects.filter(parent__isnull=True)
            .prefetch_related("category_set")
            .order_by("-updated")
        )
        if search:
            obj = obj.filter(Q(name__contains=search))
        lower = []
        data = [categoryTree(x, action, lower) for x in obj]
        if action == "low":
            data = lower
        return self.result_class(data=data)()

    @para_ok_or_400([{"name": "name", "description": "目录名称", "method": V.name}])
    def create(self, request, **kwargs):
        """
        新建产品目录
        """
        obj = m.Category.objects.get_or_create(**kwargs)
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400(
        [
            {"name": "pk", "description": "目录", "method": V.category, "replace": "obj"},
            {"name": "name", "description": "目录名称", "method": V.name},
        ]
    )
    def update(self, request, obj=None, **kwargs):
        [setattr(obj, k, v) for k, v in kwargs.items() if v]
        obj.save()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400(
        [{"name": "pk", "description": "产品", "method": V.category, "replace": "obj"}]
    )
    def destroy(self, request, obj=None, **kwargs):
        obj.delete()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400(
        [{"name": "pk", "description": "产品目录", "method": V.category, "replace": "obj"}]
    )
    def retrieve(self, request, obj=None, **kwargs):
        return self.result_class(data=obj)(serialize=True)


class ProductViewSet(ViewSet):
    serializer_class = Serializer(Product)
    """产品"""

    @para_ok_or_400(
        [
            {"name": "search", "description": "搜索字段", "method": V.name},
            {"name": "category", "description": "目录", "method": V.category},
        ]
    )
    def list(self, request, search=None, category=None, **kwargs):
        """获取产品列表"""
        query = dict()
        category and query.update(category=category)
        obj = Product.objects.filter(**query).select_related("category")
        if search:
            obj = obj.filter(
                Q(name__contains=search) | Q(category_name__contains=search)
            )
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400(
        [
            {"name": "name", "description": "产品名称", "method": V.name},
            {"name": "category", "description": "产品类别", "method": V.productCategory},
            {"name": "picture", "description": "产品图片", "type": "file"},
        ]
    )
    def create(self, request, **kwargs):
        obj = Product.objects.get_or_create(**kwargs)
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400(
        [
            {"name": "pk", "description": "产品", "method": V.product, "replace": "obj"},
            {"name": "name", "description": "产品名称", "method": V.name},
            {"name": "category", "description": "产品类别", "method": V.productCategory},
            {
                "name": "picture",
                "description": "产品图片",
                "type": "file",
                "method": V.recruitmentCategory,
            },
        ]
    )
    def update(self, request, obj=None, **kwargs):
        [setattr(obj, k, v) for k, v in kwargs.items() if v]
        obj.save()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400(
        [{"name": "pk", "description": "产品", "method": V.product, "replace": "obj"}]
    )
    def destroy(self, request, obj=None, **kwargs):
        obj.delete()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400(
        [{"name": "pk", "description": "产品", "method": V.product, "replace": "obj"}]
    )
    def retrieve(self, request, obj=None, **kwargs):
        return self.result_class(data=obj)(serialize=True)


class IndustryLinkViewSet(ViewSet):
    """
    行业链接
    """

    serializer_class = Serializer(IndustryLink)

    def list(self, request, **kwargs):
        """获取行业链接"""
        obj = IndustryLink.objects.all().order_by("rank")
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400(
        [
            {"name": "name", "description": "名称", "method": V.name},
            {"name": "link", "description": "行业链接", "method": V.url},
            {
                "name": "picture",
                "description": "背景图片",
                "method": V.file,
                "type": "file",
            },
        ]
    )
    def create(self, request, **kwargs):
        obj = IndustryLink(**kwargs)
        obj.save()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400(
        [
            {
                "name": "pk",
                "description": "行业链接",
                "method": V.industryLink,
                "replace": "obj",
            },
            {"name": "name", "description": "产品名称", "method": V.name},
            {"name": "link", "description": "行业链接", "method": V.url},
            {
                "name": "picture",
                "description": "背景图片",
                "method": V.file,
                "type": "file",
            },
        ]
    )
    def update(self, request, obj=None, **kwargs):
        [setattr(obj, k, v) for k, v in kwargs.items() if v]
        obj.save()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400(
        [
            {
                "name": "pk",
                "description": "行业链接",
                "method": V.industryLink,
                "replace": "obj",
            }
        ]
    )
    def destroy(self, request, obj=None, **kwargs):
        obj.delete()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400(
        [
            {
                "name": "pk",
                "description": "行业链接",
                "method": V.industryLink,
                "replace": "obj",
            }
        ]
    )
    def retrieve(self, request, obj=None, **kwargs):
        return self.result_class(data=obj)(serialize=True)


class SystemViewSet(ViewSet):
    """
    系统展示
    """

    serializer_class = Serializer(System, extra=["pictures", "systemCases"], dep=1)

    @method_decorator(cache_page(60 * 60))
    def list(self, request, pageSize=6, **kwargs):
        """获取系统展示"""
        obj = (
            System.objects.all()
            .prefetch_related(
                "pictures",
                "systemCases",
                "systemCases__pictures",
                "systemCases__systems",
            )
            .order_by("rank")[:pageSize]
        )
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400(
        [
            {"name": "name", "description": "名称", "method": V.name},
            {"name": "summary", "description": "简介摘要"},
            {
                "name": "summaryPicture",
                "description": "简介摘要插图",
                "method": V.file,
                "type": "file",
            },
            {"name": "introduction", "description": "系统介绍"},
            {"name": "systemFeature", "description": "系统特性"},
            {
                "name": "structure",
                "description": "系统结构",
                "method": V.file,
                "type": "file",
            },
            {"name": "funtionalFeature", "description": "功能特性"},
            {
                "name": "picture1",
                "description": "现场图片1",
                "method": V.file,
                "type": "file",
            },
            {
                "name": "picture2",
                "description": "现场图片2",
                "method": V.file,
                "type": "file",
            },
            {
                "name": "picture3",
                "description": "现场图片3",
                "method": V.file,
                "type": "file",
            },
        ]
    )
    def create(self, request, **kwargs):
        obj = System(**kwargs)
        obj.save()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400(
        [
            {"name": "pk", "description": "系统", "method": V.system, "replace": "obj"},
            {"name": "name", "description": "名称", "method": V.name},
            {"name": "summary", "description": "简介摘要"},
            {
                "name": "summaryPicture",
                "description": "简介摘要插图",
                "method": V.file,
                "type": "file",
            },
            {"name": "introduction", "description": "系统介绍"},
            {"name": "systemFeature", "description": "系统特性"},
            {
                "name": "structure",
                "description": "系统结构",
                "method": V.file,
                "type": "file",
            },
            {"name": "funtionalFeature", "description": "功能特性"},
            {
                "name": "picture1",
                "description": "现场图片1",
                "method": V.file,
                "type": "file",
            },
            {
                "name": "picture2",
                "description": "现场图片2",
                "method": V.file,
                "type": "file",
            },
            {
                "name": "picture3",
                "description": "现场图片3",
                "method": V.file,
                "type": "file",
            },
        ]
    )
    def update(self, request, obj=None, **kwargs):
        [setattr(obj, k, v) for k, v in kwargs.items() if v]
        obj.save()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400(
        [{"name": "pk", "description": "系统", "method": V.system, "replace": "obj"}]
    )
    def destroy(self, request, obj=None, **kwargs):
        obj.delete()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400(
        [{"name": "pk", "description": "系统", "method": V.system, "replace": "obj"}]
    )
    def retrieve(self, request, obj=None, **kwargs):
        return self.result_class(data=obj)(serialize=True)


class FAQsViewSet(ViewSet):
    """
    最新公告
    """

    serializer_class = Serializer(FAQs)

    @para_ok_or_400([{"name": "search", "description": "搜索"}])
    def list(self, request, search=None, **kwargs):
        """获取常见问题"""
        obj = m.FAQs.objects.all().order_by("-id")
        if search:
            obj = obj.filter(Q(title__contains=search) | Q(content__contains=search))
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400(
        [
            {"name": "title", "description": "标题"},
            {"name": "content", "description": "内容"},
        ]
    )
    def create(self, request, **kwargs):
        """
        新建常见问题
        """
        obj = m.FAQs(**kwargs)
        obj.save()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400(
        [
            {"name": "pk", "description": "常见问题", "method": V.faqs, "replace": "obj"},
            {
                "name": "title",
                "description": "标题",
                "name": "content",
                "description": "内容",
            },
        ]
    )
    def update(self, request, obj=None, **kwargs):
        """
        修改常见问题
        """
        [setattr(obj, k, v) for k, v in kwargs.items() if v]
        obj.save()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400(
        [{"name": "pk", "description": "常见问题", "method": V.faqs, "replace": "obj"}]
    )
    def destroy(self, request, obj=None, **kwargs):
        """
        删除单条常见问题
        """
        obj.delete()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400(
        [{"name": "pk", "description": "常见问题", "method": V.faqs, "replace": "obj"}]
    )
    def retrieve(self, request, obj=None, **kwargs):
        """
        获取常见问题
        """
        return self.result_class(data=obj)(serialize=True)


class NewsViewSet(ViewSet):
    """
    最新公告
    """

    serializer_class = Serializer(News)

    @para_ok_or_400(
        [
            {"name": "search", "description": "搜索"},
            {"name": "type", **V.enum(const.NEWS)},
        ]
    )
    def list(self, request, type=None, search=None, **kwargs):
        """获取新闻公告"""
        query = dict()
        type and query.update(type=type)
        obj = News.objects.filter(**query).order_by("-updated")
        if search:
            obj = obj.filter(Q(title__contains=search) | Q(content__contains=search))
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400(
        [
            {"name": "title", "description": "标题"},
            {"name": "content", "description": "内容"},
            {"name": "type", **V.enum(const.NEWS)},
        ]
    )
    def create(self, request, **kwargs):
        """
        新建新闻公告
        """
        obj = News(**kwargs)
        obj.save()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400(
        [
            {"name": "pk", "description": "新闻公告", "method": V.news, "replace": "obj"},
            {"name": "title", "description": "标题"},
            {"name": "type", **V.make(const.NEWS)},
            {"name": "content", "description": "内容"},
        ]
    )
    def update(self, request, obj=None, **kwargs):
        """
        修改单条新闻公告
        """
        [setattr(obj, k, v) for k, v in kwargs.items() if v]
        obj.save()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400(
        [{"name": "pk", "description": "新闻公告", "method": V.news, "replace": "obj"}]
    )
    def destroy(self, request, obj=None, **kwargs):
        """
        删除单条新闻公告
        """
        obj.delete()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400(
        [{"name": "pk", "description": "新闻公告", "method": V.news, "replace": "obj"}]
    )
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

    @para_ok_or_400(
        [
            {"name": "name", "description": "姓名", "method": V.name},
            {"name": "job", "description": "职位"},
            {"name": "mobile", "description": "电话", "method": V.mobile},
            {"name": "email", "description": "邮箱", "method": V.email},
            {
                "name": "attatchment",
                "description": "附件",
                "type": "file",
                "method": V.files,
                "required": True,
            },
        ]
    )
    def create(
        self,
        request,
        name=None,
        job=None,
        mobile=None,
        email=None,
        attatchment=None,
        **kwargs
    ):
        """职位申请"""
        obj = m.Job(
            name=name, job=job, mobile=mobile, email=email, attatchment=attatchment
        )
        obj.save()
        subject = "求职简历"
        content = "职位申请：\n岗位：{}\n姓名：{}\n手机：{}\n邮箱：{}\n附件为\n{}".format(
            job, name, mobile, email, ""
        )  # TODO
        send_mail(subject, content, "ssrdhr@foxmail.com")
        send_mail(subject, content, "drinks.huang@hypers.com")
        return self.result_class(data=obj)(serialize=True)


class DocumentsViewSet(ViewSet):
    """
    文档
    """

    serializer_class = Serializer(m.Documents)

    @para_ok_or_400(
        [
            {"name": "source", "required": True, **V.enum(const.SOURCES)},
            {"name": "search", "description": "搜索"},
        ]
    )
    def list(self, request, search=None, source=None, **kwargs):
        """获取文档列表"""
        obj = m.Documents.objects.all()
        if source:
            obj = obj.filter(source=source)
        if search:
            obj = obj.filter(Q(name__contains=search))
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400(
        [
            {"name": "name", "description": "名称"},
            {"name": "source", "description": dict(const.SOURCES, description="来源")},
            {
                "name": "file",
                "description": "文件",
                "type": "file",
                "method": V.file,
                "required": True,
            },
        ]
    )
    def create(self, request, **kwargs):
        """新建文档"""
        obj = m.Documents(**kwargs)
        obj.save()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400(
        [
            {"name": "pk", "method": V.document, "description": "文档", "replace": "obj"},
            {"name": "name", "description": "名称"},
            {"name": "source", "description": dict(const.SOURCES, description="来源")},
        ]
    )
    def update(self, request, obj, **kwargs):
        """更新文档"""
        [setattr(obj, k, v) for k, v in kwargs.items() if v]
        obj.save()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400(
        [{"name": "pk", "description": "文档", "method": V.document, "replace": "obj"}]
    )
    def destroy(self, request, obj=None, **kwargs):
        """
        删除单条文档
        """
        obj.delete()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400(
        [{"name": "pk", "description": "文档", "method": V.document, "replace": "obj"}]
    )
    def retrieve(self, request, obj=None, **kwargs):
        """
        获取文档
        """
        return self.result_class(data=obj)(serialize=True)


class SystemCaseViewSet(ViewSet):
    """
    系统案例
    """

    serializer_class = Serializer(m.SystemCase, extra=["pictures", "systems"])

    @method_decorator(cache_page(60 * 60))
    def list(self, request, **kwargs):
        """获取案例展示"""
        obj = m.SystemCase.objects.all()
        return self.result_class(data=obj)(serialize=True)

    @para_ok_or_400(
        [
            {
                "name": "pk",
                "description": "系统案例ID",
                "method": V.systemCase,
                "replace": "obj",
            }
        ]
    )
    def retrieve(self, request, obj=None, **kwargs):
        """
        获取文档
        """
        return self.result_class(data=obj)(serialize=True)


class TerminalViewSet(ViewSet):
    """
    远程终端访问平台
    """

    serializer_class = Serializer(m.Terminal)

    def list(self, request, **kwargs):
        """获取案例展示"""
        obj = m.Terminal.objects.all()
        return self.result_class(data=obj)(serialize=True)


class ExhibitionViewSet(ViewSet):
    """
    展会协助
    """

    serializer_class = Serializer(m.Exhibition)

    @para_ok_or_400([{"name": "type", "description": "类型 tag?"}])
    def list(self, request, type=None, **kwargs):
        """获取案例展示"""
        obj = m.Exhibition.objects.all()
        if not type:
            return self.result_class(data=obj)(serialize=True)
        obj = m.ExhibitionTag.objects.all()
        obj = Serializer(m.ExhibitionTag)(obj, many=True).data
        return self.result_class(data=obj)(serialize=False)


class EnvView(APIView):
    def get(self, request):
        """
        获取常量
        """
        domain = ("http://", "https://")[request.is_secure()] + request.get_host()
        oauth = domain + "/login/{}/"
        oauth = [dict(name=x, url=oauth.format(x)) for x in ("qq", "weibo", "weixin")]

        document = dict(const.DOCUMENTS)
        document = {y: x for x, y in document.items()}

        status = dict(const.STATUS)
        statusReverse = {y: x for x, y in status.items()}

        projectLog = {y: x for x, y in const.ProjectLog}
        projectLogReverse = {x: y for x, y in const.ProjectLog}
        projectStatus = {y: x for x, y in const.ProjectStatus}
        projectStatusReverse = {x: y for x, y in const.ProjectStatus}

        roles = {y: x for x, y in const.ROLES}
        rolesReverse = {x: y for x, y in const.ROLES}

        news = {y: x for x, y in const.NEWS}
        data = dict(
            oauth=oauth,
            document=document,
            status=status,
            statusReverse=statusReverse,
            news=news,
            roles=roles,  # {'ADMIN': 0}
            rolesReverse=rolesReverse,
            ProjectType=[x[1] for x in const.ProjectType],
            projectLog=projectLog,
            projectStatus=projectStatus,
            projectStatusReverse=projectStatusReverse,
            projectLogReverse=projectLogReverse,
        )
        return self.result_class(data)()
