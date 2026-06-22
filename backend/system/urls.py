from django.urls import path

from rest_framework.routers import DefaultRouter



from .views import (

    AdminAiLogViewSet,

    AdminConfigViewSet,

    AdminDashboardView,

    AdminModerationViewSet,

    AdminOperationLogViewSet,

    AdminUserViewSet,

    AiAdoptCopyView,

    AiBreedDetectView,

    AiQaView,

)



admin_router = DefaultRouter()

admin_router.register(r'admin/users', AdminUserViewSet, basename='admin-users')

admin_router.register(r'admin/moderation', AdminModerationViewSet, basename='admin-moderation')

admin_router.register(r'admin/config', AdminConfigViewSet, basename='admin-config')

admin_router.register(r'admin/operation-logs', AdminOperationLogViewSet, basename='admin-operation-logs')

admin_router.register(r'admin/ai-logs', AdminAiLogViewSet, basename='admin-ai-logs')



admin_user_update = AdminUserViewSet.as_view({'patch': 'partial_update'})



urlpatterns = [

    path('admin/dashboard/', AdminDashboardView.as_view(), name='admin-dashboard'),

    path('admin/users/<int:pk>/', admin_user_update, name='admin-user-update'),

    path('ai/breed-detect/', AiBreedDetectView.as_view()),

    path('ai/adopt-copy/', AiAdoptCopyView.as_view()),

    path('ai/qa/', AiQaView.as_view()),

] + admin_router.urls

