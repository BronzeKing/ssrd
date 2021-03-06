import collections
from functools import partial
import math

from rest_framework.viewsets import ViewSet as _ViewSet
from rest_framework.views import APIView as _APIView
from rest_framework.compat import coreapi
from rest_framework.pagination import BasePagination
from rest_framework.response import Response
from django.conf import settings

from paraer import Result as __Result


class Result(__Result):
    def __init__(self, data=None, errors=None, serializer=None, paginator=None):
        self.errors = errors or []
        self._error = self.errors.append
        self.serializer = serializer
        self.dataset = data
        self.paginator = paginator
        self.cookies = []

    def set_cookie(self, key, value):
        self.cookies.append((key, value))
        return self

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
            status = 400
            data = dict(msg="表单校验失败", errors=self.errors)
        if isinstance(data, collections.Iterable) and not (
            isinstance(data, dict) or hasattr(data, "_meta")
        ):
            if should_serialize:
                data = self.serializer(data, many=True).data
            data = self.paginator.paginate_queryset(
                data, self.paginator.request, paginate=paginate
            )
        elif should_serialize:
            data = self.serializer(data).data
        response = Response(data, status=status, **kwargs)
        for key, value in self.cookies:
            response.set_cookie(key, value, domain=".szssrd.com")
        return response

    def redirect(self, url):
        return Response(dict(url=url), status=302)

    def __bool__(self):
        return not bool(self.errors)


class PageNumberPager(BasePagination):
    page_size = 5
    page_query_param = "PageIndex"
    page_size_query_param = "PageSize"
    display_page_controls = False

    def paginate_queryset(self, data, request, view=None, paginate=True):
        # 传了分页参数才做分页处理
        paras = self.request.GET.get
        PageIndex = paras("pageIndex", "")
        PageSize = paras("pageSize", "")
        should_page = PageSize.isdigit() and paginate
        PageSize = PageSize.isdigit() and int(PageSize) or 10
        PageIndex = PageIndex.isdigit() and int(PageIndex) or 1
        RecordCount = len(data)
        PageCount = math.ceil(RecordCount / PageSize)
        result = dict(RecordCount=RecordCount, PageCount=PageCount, Records=data)
        if should_page:
            startRecord = (PageIndex - 1) * PageSize

            endRecord = (
                RecordCount
                if ((RecordCount - startRecord) < PageSize)
                else (startRecord + PageSize)
            )
            data = data[startRecord:endRecord]
            result = dict(RecordCount=RecordCount, PageCount=PageCount, Records=data)
        return result

    def get_schema_fields(self, view):
        fields = [
            coreapi.Field(
                name=self.page_query_param,
                required=False,
                location="query",
                description=u"分页参数：当为空时，获取全量数据",
                type="integer",
            )
        ]
        if self.page_size_query_param is not None:
            fields.append(
                coreapi.Field(
                    name=self.page_size_query_param,
                    required=False,
                    location="query",
                    description=u"分页参数：当为空时，获取全量数据",
                    type="integer",
                )
            )
        return fields


class ViewSet(_ViewSet):
    permission_classes = ()
    pagination_class = PageNumberPager
    __result_class = Result
    serializer_class = None

    @property
    def result_class(self):
        paginator = self.paginator
        paginator.request = self.request
        return partial(
            self.__result_class, serializer=self.serializer_class, paginator=paginator
        )

    @property
    def paginator(self):
        """
        The paginator instance associated with the view, or `None`.
        """
        if not hasattr(self, "_paginator"):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator


class APIView(_APIView):
    permission_classes = ()
    pagination_class = PageNumberPager
    __result_class = Result
    serializer_class = None

    @property
    def result_class(self):
        paginator = self.paginator
        paginator.request = self.request
        return partial(
            self.__result_class, serializer=self.serializer_class, paginator=paginator
        )

    @property
    def paginator(self):
        """
        The paginator instance associated with the view, or `None`.
        """
        if not hasattr(self, "_paginator"):
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


def paraerData(request):
    data = dict(request.GET.items())
    data.update(request.data.items())
    return data
