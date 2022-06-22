from django.urls import path, include
from . import views


app_name = 'dashboard'
urlpatterns = [
    path('', views.dashboardPage, name = 'dashboardPage'),
]
