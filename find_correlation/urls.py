from . import views
from django.urls import path

app_name = 'correlation'

urlpatterns = [
    path('', views.find_correlation, name = 'find_correlation')
]
