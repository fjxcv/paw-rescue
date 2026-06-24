from rest_framework.routers import DefaultRouter

from .views import LostFoundPostViewSet

router = DefaultRouter()
router.register(r'', LostFoundPostViewSet, basename='lost-found')

urlpatterns = router.urls
