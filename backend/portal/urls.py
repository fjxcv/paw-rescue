from rest_framework.routers import DefaultRouter

from .views import PortalCarouselViewSet

router = DefaultRouter()
router.register(r'carousel', PortalCarouselViewSet, basename='portal-carousel')

urlpatterns = router.urls
