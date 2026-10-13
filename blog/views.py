from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Post
from .forms import PostForm


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
def about(request):
    return render(request, 'blog/about.html')

def contact(request):
    return render(request, 'blog/contact.html')
def about(request):
    return render(request, 'blog/about.html')

def contact(request):
    return render(request, 'blog/contact.html')
def post_list(request):
    category = request.GET.get('category')
    query = request.GET.get('q')
    
    posts = Post.objects.all().order_by('-created_at')
    
    if category:
        posts = posts.filter(category=category)
    if query:
        posts = posts.filter(title__icontains=query)
        
    return render(request, 'blog/post_list.html', {
        'posts': posts,
        'current_category': category
    })

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all().order_by('-created_at')
    related_posts = Post.objects.filter(category=post.category).exclude(pk=post.pk)[:3]
    
    if request.method == 'POST':
        name = request.POST.get('name')
        body = request.POST.get('body')
        if name and body:
            Comment.objects.create(post=post, name=name, body=body)
            return redirect('post_detail', pk=post.pk)

    liked = False
    if request.user.is_authenticated and post.likes.filter(id=request.user.id).exists():
        liked = True

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'related_posts': related_posts,
        'liked': liked,
        'total_likes': post.total_likes(),
    })

def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user.is_authenticated:
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
    return redirect('post_detail', pk=pk)

def about(request):
    return render(request, 'blog/about.html')

def contact(request):
    return render(request, 'blog/contact.html')
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            if request.user.is_authenticated:
                post.author = request.user
            post.save()
            messages.success(request, "Post published successfully!")
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})
def custom_403(request, exception=None):
    return render(request, "blog/403.html", status=403)
