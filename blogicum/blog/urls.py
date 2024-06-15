from django.urls import include, path

from . import views
from .urls_prefixes import posts_prefixes

app_name = 'blog'


urlpatterns = [
    path(
        '',
        views.IndexListView.as_view(),
        name='index'
    ),
    path(
        'posts/', include(posts_prefixes)
    ),
    path(
        'category/<slug:category_slug>/',
        views.CategoryPostsListView.as_view(),
        name='category_posts'
    ),
    path(
        'profile/<str:username>/',
        views.ProfileListView.as_view(),
        name='profile'
    ),
    path(
        'edit_profile/',
        views.ProfileUpdateView.as_view(),
        name='edit_profile'
    ),
]
