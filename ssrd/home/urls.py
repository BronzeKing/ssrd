from rest_framework.routers import DefaultRouter

from django.conf.urls import include, url

from . import views

router = DefaultRouter(trailing_slash=False)

router.register(r'aboutus', views.AboutUsViewSet, base_name='aboutus')
router.register(r'faqs', views.FAQsViewSet, base_name='faqs')
router.register(r'jobs', views.JobViewSet, base_name='jobs')
router.register(r'feedBacks', views.FeedBackViewSet, base_name='feedBacks')
router.register(r'serviceNets', views.ServiceNetViewSet, base_name='serviceNets')
router.register(r'servicePromises', views.ServicePromiseViewSet, base_name='servicePromises')
router.register(r'recruitments', views.RecruitmentViewSet, base_name='recruitments')
router.register(r'products', views.ProductViewSet, base_name='products')
router.register(r'industryLinks', views.IndustryLinkViewSet, base_name='industryLinks')
router.register(r'systems', views.SystemViewSet, base_name='systems')
router.register(r'news', views.NewsViewSet, base_name='news')
urlpatterns = [
    url(r'', include(router.urls)),
]
