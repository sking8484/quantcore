from . import views
from django.urls import path

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.sign_up_view, name='sign_up_view'),
    path('login/', views.login_view, name = 'login_view'),
    path('logout/', views.logout_view, name='logout_view')
]
