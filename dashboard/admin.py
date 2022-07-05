from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(Organization)
admin.site.register(UserRole)
admin.site.register(ICD10Category)
admin.site.register(ICD10List)
