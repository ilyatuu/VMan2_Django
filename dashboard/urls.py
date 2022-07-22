from django.urls import path, include
from . import views


app_name = 'dashboard'
urlpatterns = [
    path('', views.dashboardPage, name = 'dashboardPage'),
    path('va-records/', views.vaRecordsPage, name = 'vaRecordsPage'),
    path('user-role/', views.manageRole, name = 'manageRole'),
    path('user-role/update/<str:id>/', views.updateRole, name = 'updateRole'),
    path('icd-10-category/', views.manageICD10Category, name = 'manageICD10Category'),
    path('icd-10-category/update/<str:id>/', views.updateICD10Category, name = 'updateICD10Category'),
    path('icd-10/', views.manageICD10, name = 'manageICD10'),
    path('icd-10/update/<str:id>/', views.updateICD10List, name = 'updateICD10List'),
    path('organization/', views.manageOrganization, name = 'manageOrganization'),
    path('organization/update/<str:id>/', views.updateOrganization, name = 'updateOrganization'),
    path('csmf-dataset-processing/', views.manageCSMFDataset, name = 'manageCSMFDataset'),
    path('user-authorization/', views.manageAuthorization, name = 'manageAuthorization'),
    path('user-authorization/update/<str:id>/', views.updateAuthorization, name = 'updateAuthorization'),
    path('user-authorization/delete/<str:id>/', views.deleteAuthorization, name = 'deleteAuthorization'),
    path('coding-work/', views.manageCodingWork, name = 'manageCodingWork'),
]
