import collections
from functools import partial
import math

from rest_framework.viewsets import ViewSet as _ViewSet
from rest_framework.views import APIView as _APIView
from rest_framework.compat import coreapi
from rest_framework.pagination import BasePagination
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authentication import (BasicAuthentication,
                                           SessionAuthentication, TokenAuthentication)
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from paraer import Result as __Result


class Result(__Result):
    def __init__(self, data=None, errors=None, serializer=None,
                 paginator=None):
        self.errors = errors or []
        self._error = self.errors.append
        self.serializer = serializer
        self.dataset = data
        self.paginator = paginator

    def response(self, status, serialize=False, paginate=True, **kwargs):
        """
        serialize: 是否需要序列化
        paginate: 是否需要分页
        """
        should_serialize = self.serializer and serialize
        data = self.dataset
        if status == 403:
            data = dict(msg="Permission Deny", reason=self.msg)
        elif status == 204:
            data = None
        elif self.errors:
            data = dict(msg="Validation Error", errors=self.errors)
        if isinstance(data,
                      collections.Iterable) and not (isinstance(data, dict) or hasattr(data, '_meta')):
            if should_serialize:
                data = self.serializer(data, many=True).data
            data = self.paginator.paginate_queryset(
                data, self.paginator.request, paginate=paginate)
        elif should_serialize:
            data = self.serializer(data).data
        return Response(data, status=status, **kwargs)

    def redirect(self, url):
        return Response(dict(url=url), status=302)

    def __bool__(self):
        return not bool(self.errors)


class PageNumberPager(BasePagination):
    page_size = 5
    page_query_param = 'PageIndex'
    page_size_query_param = 'PageSize'
    display_page_controls = False

    def paginate_queryset(self, data, request, view=None, paginate=True):
        # 传了分页参数才做分页处理
        paras = self.request.GET.get
        PageIndex = paras('PageIndex', '')
        PageSize = paras('PageSize', '')
        should_page = PageSize.isdigit() and paginate
        PageSize = PageSize.isdigit() and int(PageSize) or 10
        PageIndex = PageIndex.isdigit() and int(PageIndex) or 1
        RecordCount = len(data)
        PageCount = math.ceil(RecordCount / PageSize)
        result = dict(
            RecordCount=RecordCount, PageCount=PageCount, Records=data)
        if should_page:
            startRecord = (PageIndex - 1) * PageSize
            endRecord = RecordCount if ((PageCount - startRecord) <
                                        PageSize) else (startRecord + PageSize)
            data = data[startRecord:endRecord]
            result = dict(
                RecordCount=RecordCount, PageCount=PageCount, Records=data)
        return result

    def get_schema_fields(self, view):
        fields = [
            coreapi.Field(
                name=self.page_query_param,
                required=False,
                location='query',
                description=u'分页参数：当为空时，获取全量数据',
                type='integer')
        ]
        if self.page_size_query_param is not None:
            fields.append(
                coreapi.Field(
                    name=self.page_size_query_param,
                    required=False,
                    location='query',
                    description=u'分页参数：当为空时，获取全量数据',
                    type='integer'))
        return fields


TokenAuthentication.keyword = 'Bearer'


class ViewSet(_ViewSet):
    permission_classes = ()
    authentication_classes = (TokenAuthentication, SessionAuthentication, BasicAuthentication)
    pagination_class = PageNumberPager
    __result_class = Result
    serializer_class = None

    @property
    def result_class(self):
        paginator = self.paginator
        paginator.request = self.request
        return partial(
            self.__result_class,
            serializer=self.serializer_class,
            paginator=paginator)

    @property
    def paginator(self):
        """
        The paginator instance associated with the view, or `None`.
        """
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator


class APIView(_APIView):
    permission_classes = ()
    authentication_classes = (TokenAuthentication, SessionAuthentication, BasicAuthentication)
    pagination_class = PageNumberPager
    __result_class = Result
    serializer_class = None

    @property
    def result_class(self):
        paginator = self.paginator
        paginator.request = self.request
        return partial(
            self.__result_class,
            serializer=self.serializer_class,
            paginator=paginator)

    @property
    def paginator(self):
        """
        The paginator instance associated with the view, or `None`.
        """
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
                self._paginator.request = self.request
        return self._paginator


class UnAuthView(_APIView):
    serializer_class = None
    __result_class = Result

    @property
    def result_class(self):
        return partial(self.__result_class, serializer=self.serializer_class)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
        from ssrd.users.models import Profile
        Profile.objects.create(user=instance)
