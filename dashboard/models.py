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

class CSMFData(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    upload_csmf_dataset = models.FileField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    class Meta:
        verbose_name_plural = 'CSMF Data'
    def __str__(self):
        return self.id


class Authorization(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    authorize_user = models.ForeignKey(User, on_delete = models.CASCADE)
    dashboard = models.BooleanField(default = False)
    coded_va_data = models.BooleanField(default = False)
    create_graph = models.BooleanField(default = False)
    create_table = models.BooleanField(default = False)
    create_map = models.BooleanField(default = False)
    concordant_vas = models.BooleanField(default = False)
    discordant_vas = models.BooleanField(default = False)
    coding_work = models.BooleanField(default = False)
    update_profile = models.BooleanField(default = False)
    system_user = models.BooleanField(default = False)
    system_role = models.BooleanField(default = False)
    icd_10_category = models.BooleanField(default = False)
    interviewer_data = models.BooleanField(default = False)
    organization = models.BooleanField(default = False)
    upload_csmf = models.BooleanField(default = False)
    icd_10_list = models.BooleanField(default = False)
    settings = models.BooleanField(default = False)
    download_data = models.BooleanField(default = False)
    user_authorization = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        verbose_name_plural = 'Authorization List'
    def __str__(self):
        return self.authorize_user.email
