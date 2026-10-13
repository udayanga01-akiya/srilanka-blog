from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('posts/<int:pk>/', views.post_detail, name='post_detail'),
    path('like/<int:pk>/', views.like_post, name='like_post'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('post/new/', views.post_create, name='post_create'),
]