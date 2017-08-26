from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from . import views, captcha
router = DefaultRouter(trailing_slash=False)
router.register(r'users', views.UserViewSet, base_name='users')
router.register(r'authorizecodes', views.AuthorizeCodeViewSet, base_name='authorizecodes')
router.register(r'invitations', views.InvitationViewSet, base_name='invitations')
router.register(r'projects', views.ProjectViewSet, base_name='projects')
router.register(r'collects', views.CollectViewSet, base_name='collects')

urlpatterns = [
    url(regex=r'^$', view=views.UserListView.as_view(), name='list'),
    url(regex=r'^signup', view=views.UserView.as_view()),
    url(regex=r'^~redirect/$',
        view=views.UserRedirectView.as_view(),
        name='redirect'),
    url(regex=r'^(?P<username>[\w.@+-]+)/$',
        view=views.UserDetailView.as_view(),
        name='detail'),
    url(r'', include(router.urls)),
    url(r'^captcha/$', captcha.CaptchaView.as_view()),
    url(regex=r'^~update/$',
        view=views.UserUpdateView.as_view(),
        name='update'),
]
