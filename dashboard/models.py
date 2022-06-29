from django.db import models
from django.contrib.auth.models import User
import uuid

class Organization(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization_name = models.CharField(max_length = 200)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    class Meta:
        verbose_name_plural = 'Organization List'
    def __str__(self):
        return self.organization_name

class UserRole(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role_name = models.CharField(max_length = 200)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    class Meta:
        verbose_name_plural = 'Role List'
    def __str__(self):
        return self.role_name

class ICD10Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    icd10_category_name = models.CharField(max_length = 200)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    class Meta:
        verbose_name_plural = 'ICD10 Category List'
    def __str__(self):
        return self.icd10_category_name


class ICD10List(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    icd10_code = models.CharField(max_length = 50)
    icd10_name = models.CharField(max_length = 200)
    icd10_category = models.ForeignKey(ICD10Category, on_delete = models.CASCADE)
    icd10_display_name = models.CharField(max_length = 200)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    class Meta:
        verbose_name_plural = 'ICD10 List'
    def __str__(self):
        return self.icd10_name
