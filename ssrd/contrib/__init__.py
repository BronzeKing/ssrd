"""
To understand why this file is here, please read:

http://cookiecutter-django.readthedocs.io/en/latest/faq.html#why-is-there-a-django-contrib-sites-directory-in-cookiecutter-django
"""
from .utils import send_mail
from .valid import V
from .auth import ViewSet, APIView, Result, UnAuthView

__all__ = ('ViewSet', 'APIView', 'Result', 'V', 'UnAuthView', 'send_mail')
