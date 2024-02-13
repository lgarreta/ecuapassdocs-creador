from django.contrib import admin
from inquiries.models import AcademicRequests, AdministrativeRequests

# Register your models here.

admin.site.register(AcademicRequests)
admin.site.register(AdministrativeRequests)