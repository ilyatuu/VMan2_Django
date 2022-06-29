from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views


app_name = 'authentication'
urlpatterns = [
    path('user-management/', views.addNewUser, name = 'addNewUser'),
    path('login/', views.loginPage, name = 'loginPage'),
    path('logout/', auth_views.LogoutView.as_view(template_name='authentication/logout.html'), name='logout'),
]
