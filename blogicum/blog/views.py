from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.generic import ListView

from blogicum.constants import MAX_POSTS_SHOWED
from .models import Category, Post
from .forms import CommentForm, PostForm


User = get_user_model()


class IndexListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'page_obj'

    def get_queryset(self):
        return Post.published_posts.all()[:MAX_POSTS_SHOWED]


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('blog:post_detail', post_id=post_id)


def post_detail(request, post_id):
    post = get_object_or_404(
        Post.published_posts.all(),
        pk=post_id,
    )
    return render(
        request,
        'blog/detail.html',
        {
            'post': post,
            'form': CommentForm,
            'comments': post.comments.all()
        }
    )


class CategoryPostsListView(ListView):
    model = Category
    template_name = 'blog/category.html'
    context_object_name = 'page_obj'

    def get_queryset(self):
        self.category = get_object_or_404(
            Category,
            slug=self.kwargs['category_slug'],
            is_published=True,
            created_at__lte=timezone.now()
        )
        return self.category.posts.filter(
            is_published=True,
            pub_date__lte=timezone.now()
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


def create_post(request):
    form = PostForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
    context = {
        'form': form
    }
    return render(
        request,
        'blog/create.html',
        context
    )


def profile(request, username):
    profile = get_object_or_404(User, username=username)
    page_obj = Post.objects.filter(author=profile)
    return render(
        request,
        'blog/profile.html',
        context={
            'profile': profile,
            'page_obj': page_obj
        }
    )
