from django.core.cache import cache
from django.template import TemplateDoesNotExist
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.contrib.sites.shortcuts import get_current_site
from django.db import models, transaction
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.template.loader import render_to_string

from .managers import CredentialManager
from ssrd.contrib.utils import SmsClient
from ssrd import const


class Credential(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('user'),
        related_name="credentials",
        on_delete=models.CASCADE)  # 可能发送多封验证短信或者邮件， 这里保持onetoone还是ForeignKey ?
    Type = models.CharField(
        "类型",
        choices=[(k, v) for k, v in const.CredentialKeyMap.items()],
        max_length=10,
        default='email')  # 存储user的属性key，这样当user的email或者手机变更时，可以自动的获取到最新值
    verified = models.BooleanField(verbose_name=_('verified'), default=False)

    objects = CredentialManager()

    class Meta:
        verbose_name = _("credential")
        verbose_name_plural = _("credential")
        unique_together = ("user", "Type")

    def __str__(self):
        return "<Credential: %s (%s)" % (self.user, self.credential)

    __repr__ = __str__

    @property
    def credential(self):
        """
        获取手机号码或者邮箱
        """
        return getattr(self.user, self.Type)

    @property
    def captcha(self):
        return Captcha(self)

    def send_confirmation(self, request=None, action=None):
        confirmation = self.captchas()[self.Type](self.user)  # TODO 增加短信验证方式
        confirmation.send(request, action=action)
        return confirmation

    def change(self, request, new_credential, confirm=True):
        """
        Given a new email address, change self and re-confirm.
        """
        with transaction.atomic():
            setattr(self.user, self.Type, new_credential)
            self.user.save()
            self.verified = False
            self.save()
            if confirm:
                self.send_confirmation(request)

    @staticmethod
    def captchas():
        subclasses = Captcha.__subclasses__()
        return {x.name: x for x in subclasses}


def get_random_number():
    return '111111'


class Captcha(object):
    def __init__(self, user):
        self.user = user
        self.key = get_random_number()
        cache.set(
            self.user.id,
            self.key,
            timeout=settings.CREDENTIAL_CONFIRMATION_EXPIRE_DAYS)

    @classmethod
    def fromUser(cls, user, Type):
        return {x.name: x for x in cls.__subclasses__()}[Type](user)

    @classmethod
    def equal(cls, user, captcha):
        return cache.get(user.id) == captcha

    def __str__(self):
        return "<Captcha: %s>" % self.user

    __repr__ = __str__

    def __eq__(self, other):
        return self.key == other


class EmailCaptcha(Captcha):
    name = 'email'

    def send(self, request, action):
        current_site = get_current_site(request)
        ctx = {
            "user": self.user,
            "activate_url": 'http://127.0.0.1',
            "current_site": current_site,
            "captcha": self.key,
        }
        self.send_mail(action, getattr(self.user, self.name), ctx)

    def send_mail(self, template_prefix, email, context):
        msg = self.render_mail(template_prefix, email, context)
        msg.send()

    def render_mail(self, template_prefix, email, context):
        """
        Renders an e-mail to `email`.  `template_prefix` identifies the
        e-mail that is to be sent, e.g. "account/email/email_confirmation"
        """
        subject = render_to_string(
            'email/{0}_subject.txt'.format(template_prefix), context)
        # remove superfluous line breaks
        subject = " ".join(subject.splitlines()).strip()

        from_email = settings.DEFAULT_FROM_EMAIL

        bodies = {}
        for ext in ['html', 'txt']:
            try:
                template_name = 'email/{0}.{1}'.format(template_prefix, ext)
                bodies[ext] = render_to_string(template_name, context).strip()
            except TemplateDoesNotExist:
                if ext == 'txt' and not bodies:
                    # We need at least one body
                    raise
        if 'txt' in bodies:
            msg = EmailMultiAlternatives(subject, bodies['txt'], from_email,
                                         [email])
            if 'html' in bodies:
                msg.attach_alternative(bodies['html'], 'text/html')
        else:
            msg = EmailMessage(subject, bodies['html'], from_email, [email])
            msg.content_subtype = 'html'  # Main content is now text/html
        return msg

    def format_email_subject(self, subject):
        prefix = 'ssed'
        if prefix is None:
            site = get_current_site(self.request)
            prefix = "[{name}] ".format(name=site.name)
        return prefix + subject


class MobileConfirmation(Captcha):
    """
    手机验证
    """
    name = 'mobile'

    def send(self, request, action):
        """
        发送验证码
        """
        mobile = getattr(self.user, self.name)
        SmsClient.sendCaptcha(mobile, {'code': self.key})
