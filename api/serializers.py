from rest_framework import serializers
from django.contrib.auth import get_user_model  # Add this import
from .models import Video, Comment, Like  # Remove User from imports

User = get_user_model()  

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['id', 'username', 'role', 'profile_picture_url']

class VideoSerializer(serializers.ModelSerializer):
	uploader = UserSerializer(read_only=True)
	likes_count = serializers.SerializerMethodField()
	comments = serializers.SerializerMethodField()

	class Meta:
		model = Video
		fields = ['id', 'title', 'genre', 'age_rating', 'file_path', 'uploader', 'likes_count', 'comments']

	def get_likes_count(self, obj):
		return obj.likes.count()

	def get_comments(self, obj):
		comments = obj.comments.all()
		return CommentSerializer(comments, many=True).data

class CommentSerializer(serializers.ModelSerializer):
	username = serializers.CharField(source='user.username', read_only=True)
	profile_picture_url = serializers.CharField(source='user.profile_picture_url', read_only=True)

	class Meta:
		model = Comment
		fields = ['id', 'content', 'user', 'video', 'created_at', 'username', 'profile_picture_url']

class LikeSerializer(serializers.ModelSerializer):
	class Meta:
		model = Like
		fields = ['id', 'user', 'video', 'created_at']








