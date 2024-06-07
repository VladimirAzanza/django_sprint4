from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from blogicum.constants import MAX_POSTS_SHOWED
from .models import Category, Post


def index(request):
    posts = Post.published_posts.all()[:MAX_POSTS_SHOWED]
    return render(
        request,
        'blog/index.html',
        {
            'post_list': posts,
        }
    )


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


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True,
        created_at__lte=timezone.now()
    )
    posts = category.posts.filter(
        is_published=True,
        pub_date__lte=timezone.now()
    )
    return render(
        request,
        'blog/category.html',
        {
            'category': category,
            'post_list': posts,
        }
    )
