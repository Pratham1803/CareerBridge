from django.urls import path
from .views import *

urlpatterns = [
    path("manage/", manage_students, name="manage_students"),
    path("add/", add_student, name="add_student"),
    path("upload/", upload_students_excel, name="upload_students_excel"),
    path("complete-profile/", complete_profile, name="complete_profile"),
    path("dashboard/", student_dashboard, name="student_dashboard"),

]
