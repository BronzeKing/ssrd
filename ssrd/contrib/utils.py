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
