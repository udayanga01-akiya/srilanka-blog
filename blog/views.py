from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.views.generic import DetailView
from .models import Post, Comment, District
from .forms import PostForm
from .models import Post, District

# 1. මුල් පිටුව (Post List, Search & District Filter)
def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    
    # District Filter
    district_slug = request.GET.get('district') or request.GET.get('category')
    if district_slug and district_slug != 'All':
        posts = posts.filter(district__slug=district_slug)
        
    # Search Filter
    query = request.GET.get('q')
    if query:
        posts = posts.filter(Q(title__icontains=query) | Q(content__icontains=query))
        
    context = {
        'posts': posts,
        'current_category': district_slug or 'All',
    }
    return render(request, 'blog/post_list.html', context)


# 2. තනි පෝස්ට් එකක් බලන View එක (Comments & Likes සමඟ)
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all().order_by('-created_at')
    
    # අදාළ දිස්ත්‍රික්කයේම වෙනත් පෝස්ට් (Related Posts)
    related_posts = Post.objects.filter(district=post.district).exclude(pk=post.pk)[:3] if post.district else Post.objects.exclude(pk=post.pk)[:3]
    
    # Comment එකක් එකතු කිරීම
    if request.method == "POST":
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
        'total_likes': post.total_likes() if hasattr(post, 'total_likes') else 0,
    })


# 3. Like Post View
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user.is_authenticated:
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
    return redirect('post_detail', pk=post.pk)


# 4. About Page View
def about(request):
    return render(request, 'blog/about.html')


# 5. Contact Page View
def contact(request):
    return render(request, 'blog/contact.html')


# 6. Post Create View
def post_create(request):
    if request.method == "POST":
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


# 7. Custom 403 Error View
def custom_403(request, exception=None):
    return render(request, 'blog/403.html', status=403)


# 8. Post Detail Generic View
class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"

    def get_queryset(self):
        post = Post.objects.filter(status="published")
        if self.request.user.is_authenticated:
            post = Post.objects.filter(
                Q(status="published") | Q(author=self.request.user)
            )
        return post


# 9. Post Edit View
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    # 403 Permission Error පරීක්ෂාව
    if post.author != request.user:
        raise PermissionDenied

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            messages.success(request, "Post updated successfully!")
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form, 'title': 'Edit Post'})


# 10. Post Delete View
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    # 403 Permission Error පරීක්ෂාව
    if post.author != request.user:
        raise PermissionDenied

    if request.method == "POST":
        post.delete()
        messages.success(request, "Post deleted successfully!")
        return redirect('post_list')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})


# 11. Test 500 View
def test_500_view(request):
    raise Exception("This is a test 500 server error")


# 12. දිස්ත්‍රික්ක සියල්ල පෙන්වන View එක
def district_list(request):
    districts = District.objects.all()
    return render(request, 'blog/district_list.html', {'districts': districts})


# 13. තෝරාගත් දිස්ත්‍රික්කය ඇතුළේ ඇති තැන් පෙන්වන View එක
def district_detail(request, slug):
    district = get_object_or_404(District, slug=slug)
    places = district.places.all()
    return render(request, 'blog/district_detail.html', {
        'district': district,
        'places': places
    })
def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    districts = District.objects.all()
    selected_district = None
    
    # Search Filter
    query = request.GET.get('q')
    if query:
        posts = posts.filter(title__icontains=query)
        
    # District Filter
    district_id = request.GET.get('district')
    if district_id:
        selected_district = get_object_or_404(District, id=district_id)
        posts = posts.filter(district=selected_district)

    context = {
        'posts': posts,
        'districts': districts,
        'selected_district': selected_district,
    }
    return render(request, 'blog/post_list.html', context)