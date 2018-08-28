from django.urls import path
from . import views

app_name = 'regression'

urlpatterns = [
    path('', views.regression_home, name = 'regression_home'),
    path('simple_regression/', views.simple_regression, name = 'simple_regression')
]
