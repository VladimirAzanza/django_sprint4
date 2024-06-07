from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.generic import ListView

from blogicum.constants import MAX_POSTS_SHOWED
from .models import Category, Post


class IndexListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'page_obj'

    def get_queryset(self):
        return Post.published_posts.all()[:MAX_POSTS_SHOWED]


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

    return render(
        request,
        'blog/create.html',
        context={}
    )


def profile(request, username):

    return render(
        request,
        'blog/profile.html',
        context={}
    )


def logout(request):

    return render(
        request,
        'blog/index.html',
        context={}
    )
