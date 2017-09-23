import collections
import math
from functools import partial

import smtplib
from email.mime.text import MIMEText

from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication as _TokenAuthentication
from rest_framework.viewsets import ViewSet as _ViewSet
from rest_framework.views import APIView as _APIView
from rest_framework.compat import coreapi
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions
from rest_framework.pagination import BasePagination
from django.utils.six import text_type
from django.contrib.auth.models import AnonymousUser
from django.utils.translation import ugettext as _
from django.conf import settings

from paraer import Result as __Result

HTTP_HEADER_ENCODING = 'iso-8859-1'


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
                      collections.Iterable) and not isinstance(data, dict):
            if should_serialize:
                data = self.serializer(data, many=True).data
            data = self.paginator.paginate_queryset(
                data, self.paginator.request, paginate=paginate)
        elif should_serialize:
            data = self.serializer(data).data
        return Response(data, status=status, **kwargs)

    def __bool__(self):
        return not bool(self.errors)


class TokenAuthentication(_TokenAuthentication):
    def authenticate(self, request):
        header = request.META
        # 1. identify: authtoken_token.key (REST token)
        auth = header.get('HTTP_IDENTIFY', b'')
        # unicode --> iso-8859-1
        if not auth:
            return AnonymousUser, None
        if isinstance(auth, text_type):
            auth = auth.encode(HTTP_HEADER_ENCODING)
        if not auth or len(auth.split()) > 1:
            msg = _(
                'Invalid token header. Token string should not contain spaces.'
            )
            raise exceptions.AuthenticationFailed(msg)
        # iso-8859-1 --> unicode
        try:
            token = auth.decode()
        except UnicodeError:
            msg = _(
                'Invalid token header. Token string should not contain invalid characters.'
            )
            raise exceptions.AuthenticationFailed(msg)

        if token:
            return self.authenticate_credentials(token)

    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise exceptions.PermissionDenied(_(u"用户不存在"))
        if not token.user.is_authenticated:
            raise exceptions.AuthenticationFailed(_(u"无权限：管理员已注销当前用户"))
        return token.user, token


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
        should_page = PageIndex.isdigit() and PageSize.isdigit() and paginate
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


class ViewSet(_ViewSet):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    pagination_class = PageNumberPager
    __result_class = Result

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
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    pagination_class = PageNumberPager
    __result_class = Result

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


class UnSafeAPIView(_APIView):
    __result_class = Result

    @property
    def result_class(self):
        return partial(self.__result_class, serializer=self.serializer_class)


def send_mail(subject, message, to):
    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = settings.DEFAULT_FROM_EMAIL
    msg["To"] = to
    if settings.DEBUG:
        print('测试时默认不发邮件')
        return
    try:
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)
        s.login(settings.DEFAULT_FROM_EMAIL, settings.EMAIL_HOST_PASSWORD)
        s.sendmail(settings.DEFAULT_FROM_EMAIL, to, msg.as_string())
        s.quit()
        print("Success!")
    except smtplib.SMTPException as e:
        print("Falied,%s" % e)
