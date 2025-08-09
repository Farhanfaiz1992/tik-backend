# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
     VideoUploadView,SignupView, LoginView,
     VideoListView, AddCommentView, CommentListView, LikeVideoView, UnlikeVideoView,
)

router = DefaultRouter()

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('videos/upload/', VideoUploadView.as_view(), name='video-upload'),
    path('videos/', VideoListView.as_view(), name='video-list'),
    path('video/<int:video_id>/comments/add/', AddCommentView.as_view(), name='add-comment'),
    path('video/<int:video_id>/comments/', CommentListView.as_view(), name='list-comments'),
    path('video/<int:video_id>/like/', LikeVideoView.as_view(), name='like-video'),
    path('video/<int:video_id>/unlike/', UnlikeVideoView.as_view(), name='unlike-video'),
    path('', include(router.urls)),
]
