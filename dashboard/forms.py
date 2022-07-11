from django import forms
from .models import *
from django.contrib.auth.models import User
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget


class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = '__all__'
        exclude = ['created_at', 'updated_at']

class UserRoleForm(forms.ModelForm):
    class Meta:
        model = UserRole
        fields = '__all__'
        exclude = ['created_at', 'updated_at']

class ICD10CategoryForm(forms.ModelForm):
    class Meta:
        model = ICD10Category
        fields = '__all__'
        exclude = ['created_at', 'updated_at']

class ICD10ListForm(forms.ModelForm):
    class Meta:
        model = ICD10List
        fields = '__all__'
        exclude = ['created_at', 'updated_at']

class CSMFDataForm(forms.ModelForm):
    class Meta:
        model = CSMFData
        fields = '__all__'
        exclude = ['created_at', 'updated_at']

class AuthorizationForm(forms.ModelForm):
    class Meta:
        model = Authorization
        fields = '__all__'
        exclude = ['created_at', 'updated_at']
