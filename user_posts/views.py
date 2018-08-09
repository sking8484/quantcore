from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import User_Posts
from django.utils import timezone

# Create your views here.
def home_posts(request):
    posts = User_Posts.objects.order_by('-id')
    return render(request, 'user_posts/home.html', {'hello':'HELLO FROM USER_POSTS', 'posts':posts})


@login_required
def create_post(request):
    if request.method == "POST":
        if request.POST['title'] and request.POST['body'] and request.FILES['screen_shot']:
            post = User_Posts()
            post.title = request.POST['title']
            post.body = request.POST['body']
            if request.POST['URL'].startswith('http://') or request.POST['URL'].startswith('https://'):
                post.url = request.POST['URL']
            elif request.POST['URL']:
                post.url = 'http://' + request.POST['URL']

            post.image = request.FILES['screen_shot']
            post.pub_date = timezone.datetime.now()
            post.poster = request.user
            post.save()
            return redirect('/' + str(post.id))

        else:
            return render(request, 'user_posts/create.html', {'error':'All Fields except URL are required'})

    else:
        return render(request, 'user_posts/create.html')








def post_detail(request, user_posts_id):
    post = get_object_or_404(User_Posts, pk = user_posts_id)
    return render(request, 'user_posts/detail_page.html',{'post':post})
