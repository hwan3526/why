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
    path('board/<int:category_id>', board, name='board'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('signup/', signup, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('write/', write, name='write'),
    path('write/<int:blog_id>', write, name='write'),
    path('board-detail/<int:blog_id>', board_detail, name='board_detail'),
    path('board-delete/<int:blog_id>', board_delete, name='board_delete'),
    path('image-upload/', image_upload.as_view(), name='image_upload'),

    path('comment-write/<int:blog_id>', comment_write, name='comment_write'),
    path('comment-delete/<int:comment_id>', comment_delete, name='comment_delete'),
    path('comment-edit/<int:comment_id>', comment_edit, name='comment_edit'),

    path('like-comment/<int:comment_id>', like_comment_toggle, name='like_comment'),
    path('like-blog/<int:blog_id>', like_blog_toggle, name='like_blog'),

    path('accounts/profile/', board_view, name='board_view'),
]
