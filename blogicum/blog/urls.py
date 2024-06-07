from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path(
        '',
        views.IndexListView.as_view(),
        name='index'
    ),
    path(
        'posts/<int:post_id>/',
        views.post_detail,
        name='post_detail'
    ),
    path(
        'category/<slug:category_slug>/',
        views.CategoryPostsListView.as_view(),
        name='category_posts'
    ),
    path(
        'create/',
        views.create_post,
        name='create_post'
    ),
    path(
        'profile/<slug:username>',
        views.profile,
        name='profile'
    ),
    path(
        'logout/',
        views.logout,
        name='logout'
    ),
]
