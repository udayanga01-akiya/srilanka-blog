from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Post

def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    
    # 検索機能
    query = request.GET.get('q')
    if query:
        posts = posts.filter(Q(title__icontains=query) | Q(content__icontains=query))
        
    # カテゴリーフィルター
    category = request.GET.get('category')
    if category and category != 'All':
        posts = posts.filter(category=category)

    context = {
        'posts': posts,
        'current_category': category or 'All',
    }
    return render(request, 'blog/post_list.html', context)

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})