from django.urls import path
from .views import *

urlpatterns = [
    path("create/", create_company, name="create_company"),
    path("manage/", manage_companies, name="manage_companies"),
    path("complete-profile/", complete_company_profile, name="complete_company_profile"),
    path("dashboard/", company_dashboard, name="company_dashboard"),
    path("jobs/create/", create_job, name="create_job"),
    path("jobs/manage/", manage_jobs, name="manage_jobs"),
]
