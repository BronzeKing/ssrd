from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views
from paraer import get_swagger_view
from ssrd.accounts.views import LoginView, LogoutView
urlpatterns = [
    url(r'^login$', LoginView.as_view(), name='login'),
    url(r'^logout$', LogoutView.as_view(), name='account_logout'),
    url(r'^about/$',
        TemplateView.as_view(template_name='pages/about.html'),
        name='about'),
    # Django Admin, use {% url 'admin:index' %}
    url(settings.ADMIN_URL, admin.site.urls),

    # User management
    url(r'', include('ssrd.users.urls', namespace='users')),
    url(r'', include('ssrd.home.urls', namespace='home')),
    url(r'', include('ssrd.accounts.urls', namespace='accounts')),
    url('', include('social_django.urls', namespace='social'))

    # Your stuff: custom urls includes go here
]
swagger_url = not settings.DEBUG and 'https://api.mum5.cn/' or None
schema_view = get_swagger_view(title='ssrd', url=swagger_url)
urlpatterns += [
    url(r'^docs', schema_view),
    url(r'^$', schema_view, name='home'),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$',
            default_views.bad_request,
            kwargs={'exception': Exception('Bad Request!')}),
        url(r'^403/$',
            default_views.permission_denied,
            kwargs={'exception': Exception('Permission Denied')}),
        url(r'^404/$',
            default_views.page_not_found,
            kwargs={'exception': Exception('Page not Found')}),
        url(r'^500/$', default_views.server_error),
    ]
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
