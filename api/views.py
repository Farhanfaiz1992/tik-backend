from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, get_user_model  # Changed import
from django.contrib.auth.models import update_last_login
from django.conf import settings
from .models import Video, Comment, Like  # Removed User import
from .serializers import UserSerializer, VideoSerializer, CommentSerializer, LikeSerializer
from django.core.files.storage import default_storage
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model() 
# User Registration
class SignupView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        role = request.data.get('role', 'consumer')
        profile_picture = request.FILES.get('profile_picture')

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

        user = User(username=username, role=role)
        user.set_password(password)
        path = default_storage.save(f'profile_pics/{profile_picture.name}', profile_picture)

        
        user.profile_picture_url = f'https://{settings.AZURE_ACCOUNT_NAME}.blob.core.windows.net/{settings.AZURE_MEDIA_CONTAINER}/{path}'  # Prod URL
        
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# User Login
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        
        update_last_login(None, user)
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        })


# Video Upload
class VideoUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        title = request.data.get('title')
        genre = request.data.get('genre')
        age_rating = request.data.get('age_rating')
        file = request.FILES.get('file')
        print("Auth Header:", request.headers.get('Authorization'))
        print("Authenticated User:", request.user)
        if not file:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        path = default_storage.save(f'videos/{file.name}', file)
        file_path = f'https://{settings.AZURE_ACCOUNT_NAME}.blob.core.windows.net/{settings.AZURE_MEDIA_CONTAINER}/{path}'
        print("File Path:", file_path)
        video = Video.objects.create(
            title=title,
            genre=genre,
            age_rating=age_rating,
            file_path=file_path,
            uploader=request.user
        )
        print("Video:", video)
        serializer = VideoSerializer(video)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# List Videos
class VideoListView(generics.ListAPIView):
    queryset = Video.objects.all().select_related('uploader').prefetch_related('comments', 'likes')
    serializer_class = VideoSerializer
    permission_classes = [permissions.AllowAny]

# Add Comment
class AddCommentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, video_id):
        video = Video.objects.filter(id=video_id).first()
        print("Received data:", request.data)  # Debug log
        print("Headers:", request.headers)    # Debug log
        content = request.data.get('content')
        if not video:
            return Response({'error': 'Video not found'}, status=status.HTTP_404_NOT_FOUND)
        comment = Comment.objects.create(content=content, user=request.user, video=video)
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# List Comments
class CommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        video_id = self.kwargs['video_id']
        return Comment.objects.filter(video_id=video_id)

# Like Video
class LikeVideoView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, video_id):
        video = Video.objects.filter(id=video_id).first()
        if not video:
            return Response({'error': 'Video not found'}, status=status.HTTP_404_NOT_FOUND)
        like, created = Like.objects.get_or_create(user=request.user, video=video)
        if not created:
            return Response({'message': 'Already liked'})
        return Response({'message': 'Liked'})

# Unlike Video
class UnlikeVideoView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, video_id):
        video = Video.objects.filter(id=video_id).first()
        if not video:
            return Response({'error': 'Video not found'}, status=status.HTTP_404_NOT_FOUND)
        like = Like.objects.filter(user=request.user, video=video).first()
        if not like:
            return Response({'message': 'Not liked yet'})
        like.delete()
        return Response({'message': 'Unliked'})
