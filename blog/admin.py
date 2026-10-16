from django.contrib import admin
from .models import Post, District, Comment

# District Model එක Register කිරීම
@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# Post Model එක Register කිරීම
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'district', 'created_at')
    list_filter = ('district', 'created_at')
    search_fields = ('title', 'content')

# Comment Model එක Register කිරීම
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at')