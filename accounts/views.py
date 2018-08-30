from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth


def sign_up_view(request):
    if request.method == 'POST':

        if (request.POST['password1'] == request.POST['password2']) and (request.POST['email1'] == request.POST['email2']):
            try:
                user = User.objects.get(username=request.POST['username'])
                return render(request, 'accounts/sign_up.html', {'error':'This username already exists'})
            except User.DoesNotExist:
                user = User.objects.create_user(request.POST['username'], password = request.POST['password1'], email=request.POST['email1'])
                auth.login(request, user)
                return redirect('user_posts:home')
        else:
            return render(request, 'accounts/sign_up.html', {'error': 'The passwords must match'})

    else:
        return render(request, 'accounts/sign_up.html',{})

def login_view(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'], password = request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect('user_posts:home')
        else:
            return render(request, 'accounts/login.html', {'error':'There is no user with those credentials'})


    return render(request, 'accounts/login.html', {})

def logout_view(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('user_posts:home')
    return render(request, 'accounts/login.html', {})
