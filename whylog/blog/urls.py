from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter
from django.contrib.auth import views as auth_views

router = DefaultRouter()
router.register(r'blog', BlogViewSet)
router.register(r'user', UserViewSet)
router.register(r'comment', CommentViewSet)
router.register(r'like', LikeViewSet)
router.register(r'alarm', AlarmViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('', board, name='board'),
    path('board/', board, name='board'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('write/', write, name='write'),
    path('board-detail/<int:blog_id>', board_detail, name='board_detail'),

    path('accounts/profile/', board_view, name='board_view'),
]
