# Create your views here.
import openpyxl
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from .models import *
from django.contrib.auth.decorators import login_required, user_passes_test

CustomUser = get_user_model()

def is_tpo(user):
    return user.is_authenticated and (user.role == "TPO" or user.is_superuser)

@login_required
@user_passes_test(is_tpo)
def manage_students(request):
    students = StudentProfile.objects.all()
    return render(request, "students/manage_students.html", {"students": students})

@login_required
@user_passes_test(is_tpo)
def add_student(request):
    if request.method == "POST":
        student_id = request.POST["student_id"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        password = request.POST["student_id"]  # Or generate from DOB later

        user = CustomUser.objects.create_user(
            username=student_id,
            email=email,
            password=password,
            role="STUDENT"
        )
        StudentProfile.objects.create(
            user=user,
            student_id=student_id,
            first_name=first_name,
            last_name=last_name
        )
        return redirect("manage_students")
    return render(request, "students/add_student.html")

@login_required
@user_passes_test(is_tpo)
def upload_students_excel(request):
    if request.method == "POST" and request.FILES["excel_file"]:
        excel_file = request.FILES["excel_file"]
        wb = openpyxl.load_workbook(excel_file)
        sheet = wb.active

        for row in sheet.iter_rows(min_row=2, values_only=True):
            student_id, first_name, last_name, email = row
            if not CustomUser.objects.filter(username=student_id).exists():
                user = CustomUser.objects.create_user(
                    username=student_id,
                    email=email,
                    password="defaultpass123",
                    role="STUDENT"
                )
                StudentProfile.objects.create(
                    user=user,
                    student_id=student_id,
                    first_name=first_name,
                    last_name=last_name
                )
        return redirect("manage_students")
    return render(request, "students/upload_students.html")

@login_required
def complete_profile(request):
    profile = get_object_or_404(StudentProfile, user=request.user)

    if request.method == "POST":
        # Personal Info
        profile.first_name = request.POST.get("first_name")
        profile.last_name = request.POST.get("last_name")
        profile.gender = request.POST.get("gender")
        profile.dob = request.POST.get("dob")

        # Contact Info
        profile.email_college = request.POST.get("email_college")
        profile.email_personal = request.POST.get("email_personal")
        profile.phone_number = request.POST.get("phone_number")
        profile.city = request.POST.get("city")
        profile.permanent_address = request.POST.get("permanent_address")

        # Academics
        profile.tenth_percentage = request.POST.get("tenth_percentage") or None
        profile.twelfth_percentage = request.POST.get("twelfth_percentage") or None
        profile.bachelor_college = request.POST.get("bachelor_college")
        profile.bachelor_course = request.POST.get("bachelor_course")
        profile.bachelor_cgpa = request.POST.get("bachelor_cgpa") or None

        profile.master_college = request.POST.get("master_college")
        profile.master_course = request.POST.get("master_course")
        profile.master_cgpa = request.POST.get("master_cgpa") or None

        # Extra Info
        profile.active_backlogs = request.POST.get("active_backlogs") or 0
        profile.batch_year = request.POST.get("batch_year") or None

        # Skills (many-to-many)
        skill_ids = request.POST.getlist("skills")
        profile.skills.set(Skill.objects.filter(id__in=skill_ids))

        # Online Profiles
        profile.linkedin_url = request.POST.get("linkedin_url")
        profile.github_url = request.POST.get("github_url")
        profile.portfolio_url = request.POST.get("portfolio_url")

        # Resume
        profile.resume_link = request.POST.get("resume_link")

        # Set status active if everything important filled
        if (
            profile.first_name and profile.last_name and
            profile.phone_number and profile.resume_link
        ):
            profile.status = "ACTIVE"

        profile.save()
        return redirect("student_dashboard")

    

    # Pass choices directly to template
    bachelor_choices = StudentProfile._meta.get_field("bachelor_course").choices
    master_choices = StudentProfile._meta.get_field("master_course").choices

    all_skills = Skill.objects.all()
    return render(
        request,
        "students/complete_profile.html",
        {
            "profile": profile,
            "skills": all_skills,
            "bachelor_choices": bachelor_choices,
            "master_choices": master_choices,
        },
    )

@login_required
def student_dashboard(request):
    # Ensure only students can access this
    if request.user.role != "STUDENT":
        return redirect("login")

    profile = get_object_or_404(StudentProfile, user=request.user)

    return render(
        request,
        "students/student_dashboard.html",
        {
            "profile": profile,
        },
    )