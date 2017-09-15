from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views
from ssrd.contrib import TokenView
from paraer import get_swagger_view
schema_view = get_swagger_view(title='ssrd')
urlpatterns = [
    url(r'^$', schema_view, name='home'),
    url(r'^about/$', TemplateView.as_view(template_name='pages/about.html'), name='about'),
    url(r'^docs', schema_view),
    url(r'token$', TokenView.as_view()),
    # Django Admin, use {% url 'admin:index' %}
    url(settings.ADMIN_URL, admin.site.urls),

    # User management
    url(r'', include('ssrd.users.urls', namespace='users')),
    url(r'', include('social.apps.django_app.urls', namespace='socail')),
    url(r'', include('ssrd.home.urls', namespace='home')),
    url(r'^accounts/', include('allauth.urls')),
    # Your stuff: custom urls includes go here
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        url(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        url(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        url(r'^500/$', default_views.server_error),
    ]
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
