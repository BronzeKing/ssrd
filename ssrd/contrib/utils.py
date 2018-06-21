try:
    from aliyunsms.services import BaseClient
except Exception:
    class BaseClient:
        pass
from django.conf import settings
from django.core.mail import send_mail as _send_mail


def send_mail(subject, message, to):
    if not isinstance(to, list):
        to = [to]
    if settings.DEBUG:
        print("调试模式下不打开发邮件")
        print(subject)
        print(message)
        print(to)
        return
    _send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, to)


class SmsClient(BaseClient):

    @classmethod
    def sendCaptcha(cls, phoneNumbers, param):
        """
        @phoneNumbers 手机号码 170xxxxxxxx 或[170xxxxxxxx]
        @param 短信模板参数 {'code': 'xxxx'}
        """
        instance = cls(settings.ALIYUN_ACCESSKEY_ID, settings.ALIYUN_ACCESSKEY_SECRET)
        return instance.send_sms(phoneNumbers, settings.ALIYUN_SIGN, settings.ALIYUN_TEMPLATE_CODE, param)
