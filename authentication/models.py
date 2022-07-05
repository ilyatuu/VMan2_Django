from django.db import models
from django.contrib.auth.models import User
import uuid
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from dashboard.models import *

class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    user_token = models.CharField(max_length=3000)
    organization = models.ForeignKey(Organization, on_delete = models.CASCADE)
    user_role = models.ForeignKey(UserRole, on_delete = models.CASCADE)
    nationality = CountryField()
    mobile_number = PhoneNumberField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    class Meta:
        verbose_name_plural = 'Profile'
    def __str__(self):
        return self.user.username
