from django.contrib import admin
from .models import Company, Job, EligibleCourse

admin.site.register(Company)
admin.site.register(Job)
admin.site.register(EligibleCourse)
