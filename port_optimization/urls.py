from django.urls import path
from . import views

app_name = 'portfolio_optimization'

urlpatterns = [
    path('', views.optimize, name = 'optimize')
]
