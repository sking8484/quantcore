from django.urls import path
from . import views

app_name = 'about'

urlpatterns = [
    path('data/', views.about_data_page, name = 'about_data_page'),
    path('strategies/', views.about_strategies_page, name = 'about_strategies_page')
]
