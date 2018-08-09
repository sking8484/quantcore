from django.urls import path, include
from django.shortcuts import redirect
from . import views

app_name = 'data'

urlpatterns = [

    path('data/', views.get_the_data, name = 'get_the_data'),
]
