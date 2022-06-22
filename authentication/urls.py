from django.urls import path, include
from . import views


app_name = 'authentication'
urlpatterns = [
    path('login/', views.loginPage, name = 'loginPage'),
]
