from typing import Any
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.urls import reverse
from django.views.generic import DeleteView, ListView, UpdateView

from blogicum.constants import MAX_POSTS_SHOWED
from .models import Category, Post, Comment
from .forms import CommentForm, PostForm, UserForm


User = get_user_model()


class OnlyAuthorMixin(UserPassesTestMixin):

    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user


class IndexListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    paginate_by = 10

    def get_queryset(self):
        return Post.published_posts.all()


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
            'form': CommentForm(),
            'comments': post.comments.all()
        }
    )


class EditPostUpdateView(LoginRequiredMixin, OnlyAuthorMixin, UpdateView):
    model = Post
    template_name = 'blog/create.html'
    form_class = PostForm

    def dispatch(self, request, *args, **kwargs):
        if not self.test_func():
            return redirect('blog:post_detail', post_id=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


def delete_post(request, post_id):
    post_instance = get_object_or_404(Post, pk=post_id)
    form = PostForm(instance=post_instance)
    context = {
        'form': form
    }
    if request.method == 'POST':
        post_instance.delete()
        return redirect('blog:index')
    return render(
        request,
        'blog/create.html',
        context
    )


class CommentUpdateView(UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'


class CommentDeleteView(DeleteView):
    model = Comment
    template_name = 'blog/comment.html'

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.object.post.id}
        )


class CategoryPostsListView(ListView):
    model = Category
    template_name = 'blog/category.html'
    paginate_by = 10

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


@login_required
def create_post(request):
    form = PostForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('blog:profile', username=post.author.username)
    context = {
        'form': form
    }
    return render(
        request,
        'blog/create.html',
        context
    )


class ProfileListView(ListView):
    model = Post
    template_name = 'blog/profile.html'
    paginate_by = 10

    def get_queryset(self):
        self.profile = get_object_or_404(
            User,
            username=self.kwargs['username'])
        return Post.objects.filter(author=self.profile)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.profile
        return context


def edit_profile(request):
    user_instance = get_object_or_404(User, username=request.user.username)
    form = UserForm(request.POST or None, instance=user_instance)
    if form.is_valid():
        form.save()
        return redirect('blog:profile', username=request.user.username)
    return render(
        request,
        'blog/user.html',
        context={
            'form': form
        }
    )
