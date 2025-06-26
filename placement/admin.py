from django.contrib import admin
from .models import Company, JobApplication

admin.site.register(Company)
admin.site.register(JobApplication)


class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'application_deadline', 'interview_date']