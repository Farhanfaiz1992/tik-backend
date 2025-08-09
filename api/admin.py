from django.contrib import admin
from .models import User, Video, Comment, Like

# Register User model with custom admin
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'profile_picture_url', 'date_joined', 'last_login')
    search_fields = ('username', 'email')
    list_filter = ('role',)
    ordering = ('username',)
    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'password')
        }),
        ('Permissions', {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser')
        }),
        ('Important Dates', {
            'fields': ('date_joined', 'last_login')
        }),
        ('Profile', {
            'fields': ('profile_picture_url',)
        }),
    )

# Register Video model with custom admin
@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'age_rating', 'file_path', 'uploader')
    search_fields = ('title', 'genre', 'age_rating')
    list_filter = ('genre', 'age_rating')
    ordering = ('-id',)

# Register Comment model with custom admin
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'user', 'video', 'created_at')
    search_fields = ('content',)
    list_filter = ('created_at',)
    ordering = ('-created_at',)

# Register Like model with custom admin
@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'video', 'created_at')
    search_fields = ('user__username', 'video__title')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
