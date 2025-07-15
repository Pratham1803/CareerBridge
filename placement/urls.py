from django.urls import path
from . import views

urlpatterns = [
    path('/', views.company_list, name='company_list'),
    path('companies/<int:pk>/', views.company_detail, name='company_detail'),  # <-- new
    path('companies/<int:pk>/apply/', views.apply_to_company, name='apply_to_company'),
    path('applications/', views.applied_jobs, name='applied_jobs'),
    path('applications/<int:application_id>/withdraw/', views.withdraw_application, name='withdraw_application'),
    path('export/companies/', views.export_companies_excel, name='export_companies_excel'),
    path('export/applied/', views.export_applied_jobs_excel, name='export_applied_jobs_excel'),    
]
