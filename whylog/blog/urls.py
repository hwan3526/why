from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'blog', BlogViewSet)
router.register(r'user', UserViewSet)
router.register(r'comment', CommentViewSet)
router.register(r'like', LikeViewSet)
router.register(r'alram', AlarmViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
