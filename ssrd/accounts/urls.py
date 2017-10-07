from django.conf.urls import url

from .views import LoginView, PasswordResetView, PasswordChangeView, CredentialView, RegisterView, CaptchaView

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='account_login'),
    url(r'^register', RegisterView.as_view(), name='account_signup'),
    url(r'^credential$', CredentialView.as_view()),
    url(r'^captcha$', CaptchaView.as_view()),
    url(r'^password/change$', PasswordChangeView.as_view()),
    url(r'^password/reset$', PasswordResetView.as_view()),
]
