from django.urls import path
from . import views

urlpatterns = [    
    path('send-reminders/', views.send_interview_reminders_view, name='send_interview_reminders'),

    # New Urls at testing 
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('admin/dashboard-stats/', views.admin_dashboard_stats, name='admin_dashboard_stats'),
    path('admin/companies/', views.admin_company_list, name='admin_company_list'),
    path('admin/companies/create/', views.admin_company_create, name='admin_company_create'),
    path('admin/companies/<int:company_id>/edit/', views.admin_company_edit, name='admin_company_edit'),
    path('admin/companies/<int:company_id>/delete/', views.admin_company_delete, name='admin_company_delete'),
    path('admin/students/', views.admin_student_list, name='admin_student_list'),
    path('admin/selected-students/', views.admin_selected_students, name='admin_selected_students'),
    path('admin/users/', views.admin_user_management, name='admin_user_management'),
    path('admin/users/create/', views.admin_user_create, name='admin_user_create'),
    path('admin/users/<int:user_id>/edit/', views.admin_user_edit, name='admin_user_edit'),
    path('admin/users/<int:user_id>/delete/', views.admin_user_delete, name='admin_user_delete'),
    path('admin/users/<int:user_id>/reset-password/', views.admin_user_reset_password, name='admin_user_reset_password'),
    path('admin/users/<int:user_id>/toggle-active/', views.admin_user_toggle_active, name='admin_user_toggle_active'),
    path('admin/placement-tracking/', views.admin_placement_tracking, name='admin_placement_tracking'),
    path('admin/notify-students/', views.admin_notify_students, name='admin_notify_students'),
    path('admin/export-report-excel/', views.admin_export_report_excel, name='admin_export_report_excel'),
    path('admin/report/', views.admin_report, name='admin_report'),
    path('admin/export-report-pdf/', views.admin_export_report_pdf, name='admin_export_report_pdf'),
    path('admin/profile/', views.admin_profile, name='admin_profile'),
    path('admin/toggle-selected/<int:app_id>/', views.admin_toggle_selected, name='admin_toggle_selected'),
]
