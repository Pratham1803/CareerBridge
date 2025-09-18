from django.urls import path
from .views import *

urlpatterns = [
    path("create-tpo/", create_tpo, name="create_tpo"),
    path("tpo/dashboard/", tpo_dashboard, name="tpo_dashboard"),
    path("", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("tpo/dashboard/", tpo_dashboard, name="tpo_dashboard"),
]



# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.student_dashboard, name='student_home'),
#     path('login/', views.login_view, name='login'),
#     path('register/', views.register_student, name='register'),
#     path('logout/', views.logout_view, name='logout'),
#     path('profile/', views.student_profile, name='student_profile'),
# ]