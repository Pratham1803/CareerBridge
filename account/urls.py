from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_student, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.student_profile, name='student_profile'),
]
