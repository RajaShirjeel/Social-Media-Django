from django.urls import path
from .import views

app_name = 'posts'

urlpatterns = [
    path('', views.PostList.as_view(), name='all'),
    path('create_post', views.CreatePost.as_view(), name='create'),
    path('by/<username>/<int:pk>', views.PostDetail.as_view(), name='single'),
    path('by/<username>', views.UserPosts.as_view(), name='user_posts'),
    path('delete/<int:pk>', views.DeletePost.as_view(), name='delete')
]