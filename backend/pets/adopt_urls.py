from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    AdminAdoptApplicationViewSet,
    AdminOfflineVerifyViewSet,
    AdoptApplicationViewSet,
)

adopt_router = DefaultRouter()
adopt_router.register(r'applications', AdoptApplicationViewSet, basename='adopt-application')

admin_adopt = AdminAdoptApplicationViewSet.as_view({'put': 'update', 'patch': 'update'})
admin_verify = AdminOfflineVerifyViewSet.as_view({'put': 'update', 'patch': 'update'})

urlpatterns = adopt_router.urls + [
    path('applications/<int:pk>/audit/', admin_adopt, name='admin-adopt-audit'),
    path('offline-verify/<int:pk>/', admin_verify, name='admin-offline-verify'),
]
