from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from . import views
router = DefaultRouter(trailing_slash=False)
router.register(r'users', views.UserViewSet, base_name='users')
router.register(r'authorizecodes', views.AuthorizeCodeViewSet, base_name='authorizecodes')
router.register(r'invitations', views.InvitationViewSet, base_name='invitations')
router.register(r'projects', views.ProjectViewSet, base_name='projects')
router.register(r'collects', views.CollectViewSet, base_name='collects')
router.register(r'messages', views.MessageViewSet, base_name='messages')

urlpatterns = [
    url(regex=r'^signup', view=views.UserView.as_view()),
    url(regex=r'^~redirect/$',
        view=views.UserRedirectView.as_view(),
        name='redirect'),
    url(r'', include(router.urls)),
]
