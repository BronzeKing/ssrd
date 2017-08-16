from rest_framework.routers import DefaultRouter

from django.conf.urls import include, url

from .views import AboutUsViewSet, FAQsViewSet, FeedBackViewSet, ServiceNetViewSet, ServicePromiseViewSet, RecruitmentViewSet, ProductViewSet

router = DefaultRouter(trailing_slash=False)

router.register(r'aboutus', AboutUsViewSet, base_name='aboutus')
router.register(r'faqs', FAQsViewSet, base_name='faqs')
router.register(r'feedBacks', FeedBackViewSet, base_name='feedBacks')
router.register(r'serviceNets', ServiceNetViewSet, base_name='serviceNets')
router.register(r'servicePromises', ServicePromiseViewSet, base_name='servicePromises')
router.register(r'recruitments', RecruitmentViewSet, base_name='recruitments')
router.register(r'products', ProductViewSet, base_name='products')
urlpatterns = [
    url(r'', include(router.urls)),
]
