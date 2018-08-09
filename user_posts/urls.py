from . import views
from django.urls import path

app_name = 'user_posts'

urlpatterns = [
    path('', views.home_posts, name = 'home'),
    path('create_post/', views.create_post, name = 'create_post' ),
    path('<int:user_posts_id>', views.post_detail, name = 'post_detail')
]
