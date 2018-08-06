from django.urls import path, include
from django.shortcuts import redirect
from . import views

app_name = 'data'

urlpatterns = [
    path('', views.home, name = 'home'),
    path('data/', views.get_the_data, name = 'get_the_data'),
]
