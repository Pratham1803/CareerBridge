from django.urls import path
from . import views

urlpatterns = [    
    path('send-reminders/', views.send_interview_reminders_view, name='send_interview_reminders'),

    # New Urls at testing 
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard-stats/', views.admin_dashboard_stats, name='admin_dashboard_stats'),
    path('companies/', views.admin_company_list, name='admin_company_list'),
    path('companies/create/', views.admin_company_create, name='admin_company_create'),
    path('companies/<int:company_id>/edit/', views.admin_company_edit, name='admin_company_edit'),
    path('companies/<int:company_id>/delete/', views.admin_company_delete, name='admin_company_delete'),
    path('students/', views.admin_student_list, name='admin_student_list'),
    path('selected-students/', views.admin_selected_students, name='admin_selected_students'),
    path('users/', views.admin_user_management, name='admin_user_management'),
    path('users/create/', views.admin_user_create, name='admin_user_create'),
    path('users/<int:user_id>/edit/', views.admin_user_edit, name='admin_user_edit'),
    path('users/<int:user_id>/delete/', views.admin_user_delete, name='admin_user_delete'),
    path('users/<int:user_id>/reset-password/', views.admin_user_reset_password, name='admin_user_reset_password'),
    path('users/<int:user_id>/toggle-active/', views.admin_user_toggle_active, name='admin_user_toggle_active'),
    path('placement-tracking/', views.admin_placement_tracking, name='admin_placement_tracking'),
    path('notify-students/', views.admin_notify_students, name='admin_notify_students'),
    path('export-report-excel/', views.admin_export_report_excel, name='admin_export_report_excel'),
    path('report/', views.admin_report, name='admin_report'),
    path('export-report-pdf/', views.admin_export_report_pdf, name='admin_export_report_pdf'),
    path('profile/', views.admin_profile, name='admin_profile'),
    path('toggle-selected/<int:app_id>/', views.select_student_for_company, name='admin_toggle_selected'),
]
