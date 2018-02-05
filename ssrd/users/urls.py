from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from . import views
router = DefaultRouter(trailing_slash=False)
router.register(r'users', views.UserViewSet, base_name='users')
router.register(r'groups', views.GroupViewSet, base_name='groups')
router.register(r'authorizeCodes', views.AuthorizeCodeViewSet, base_name='authorizeCodes')
router.register(r'invitations', views.InvitationViewSet, base_name='invitations')
router.register(r'projects', views.ProjectViewSet, base_name='projects')
router.register(r'projectGroups', views.ProjectGroupViewSet, base_name='projectGroups')
router.register(r'collects', views.CollectViewSet, base_name='collects')
router.register(r'messages', views.MessageViewSet, base_name='messages')
router.register(r'attatchment', views.DocumentsViewSet, base_name='attatchment')
router.register(r'directories', views.DirectoryViewSet, base_name='directories')
router.register(r'medias', views.MediaViewSet, base_name='medias')
router.register(r'projects/(?P<projectId>\d+)/logs', views.ProjectLogViewSet, base_name='logs')

urlpatterns = [
    url(regex=r'^signup$', view=views.UserView.as_view()),
    url(r'^users/(?P<user>\d+)/profile$', view=views.ProfileView.as_view()),
    url(r'^carts', view=views.CartView.as_view()),
    url(regex=r'^~redirect/$',
        view=views.UserRedirectView.as_view(),
        name='redirect'),
    url(r'', include(router.urls)),
]
