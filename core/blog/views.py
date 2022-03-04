from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.views.generic import CreateView, UpdateView
from django.contrib import messages
from .models import Post, Comment, Category
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse

"""MainView"""
def MainView(request):
    posts = Post.objects.filter(visible=True)
    categories = Category.objects.all()
    category = ''
    if request.method == 'GET':
        if 'category' in request.GET:
            category = request.GET['category']
            if category != 'All':
                posts = Post.objects.filter(category__name=category, visible=True)
    ctx = {'posts' : posts.order_by('-post_date'), 'category' : category, 'categories' : categories}
    return render(request, 'blog/mainview.html', ctx)


"""PostDetail View"""
def PostDetailView(request, pk):
    post = Post.objects.get(pk=pk)
    if post.visible == True or request.user.is_superuser or post.author == request.user:
        if request.method == 'POST':
            name = request.POST.get('name')
            comment = request.POST.get('comment')
            comment = Comment(body=comment, author=name, post=post, visible=True)
            comment.save()
            messages.info(request, 'Thank you for your comment. It is sent for review and will appear under the post very soon.')
        comments = Comment.objects.filter(post=post, visible=True)
        ctx = {'post': post, 'comments' : comments}
        return render(request, 'blog/postview.html', ctx)
    else:
        return redirect('compapp:NoAccess')

"""Like Posts View"""
def LikePost(request, pk):
    post = Post.objects.get(pk=pk)
    post.likes = post.likes + 1
    post.save()
    messages.info(request, 'I\'m glad you liked the article. Thank you for reading!')
    return redirect('blog:PostDetailView', pk)

"""Post Create View"""
@method_decorator(login_required(), 'dispatch')
class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'body', 'snippet', 'category']
    success_url = reverse_lazy('blog:MainView')
    """finction which check if form is valid"""
    def form_valid(self, form):
        object = form.save(commit=False)
        object.author = self.request.user
        object.save()
        post = Post.objects.get(pk=object.pk)
        messages.info(self.request, 'Your post is saved and sent for review. Once it is approved, it will be published.')
        return super(PostCreateView, self).form_valid(form)

"""Post Edit View"""
@method_decorator(login_required(), 'dispatch')
class PostEditView(UpdateView):
    model = Post
    fields = ['title', 'body', 'snippet', 'category']
    success_url = reverse_lazy('blog:MainView')
    def get_queryset(self):
        qs = super(PostEditView, self).get_queryset()
        if self.request.user.is_superuser:
            return qs
        else:
            return qs.filter(author=self.request.user, locked=False)

"""My Artile View"""
@login_required()
def MyArticlesView(request):
    posts = Post.objects.filter(author=request.user)
    categories = []
    for post in posts:
        if not post.category in categories:
            categories.append(post.category)
    category = ''
    if request.method == 'GET':
        if 'category' in request.GET:
            category = request.GET['category']
            if category != 'All':
                posts = posts.filter(category__name=category)
    ctx = {'posts' : posts.order_by('-post_date'), 'category' : category, 'categories' : categories, 
        'view' : 'MyArticlesView'}
    return render(request, 'blog/mainview.html', ctx)

"""If post is not access"""
def NoAccess(request):
    return render(request, 'blog/noaccess.html')

"""Dlete the post"""
def delete_blog_view(request, pk):
    context = {}
    user = request.user
    """check if  user is authenticated"""
    if not user.is_authenticated:
        return HttpResponse("You must be authenticated")
    """if authenticated"""
    blog_post = get_object_or_404(Post, pk=pk)
    if request.POST:
        blog_post.delete()
        return redirect('blog:MainView')

    return render(request, 'blog/delete.html', context)

