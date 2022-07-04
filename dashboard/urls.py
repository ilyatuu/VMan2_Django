from django.urls import path, include
from . import views


app_name = 'dashboard'
urlpatterns = [
    path('', views.dashboardPage, name = 'dashboardPage'),
    path('user-role/', views.manageRole, name = 'manageRole'),
    path('icd-10-category/', views.manageICD10Category, name = 'manageICD10Category'),
    path('icd-10/', views.manageICD10, name = 'manageICD10'),
    path('organization/', views.manageOrganization, name = 'manageOrganization'),
]
