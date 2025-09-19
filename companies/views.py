from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Company, Job
from students.models import COURSE_CHOICES

CustomUser = get_user_model()

def is_tpo(user):
    return user.is_authenticated and (user.role == "TPO" or user.is_superuser)

@login_required
@user_passes_test(is_tpo)
def create_company(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        name = request.POST["name"]

        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            role="COMPANY"
        )

        Company.objects.create(
            user=user,
            name=name,
            hr_email=email
        )
        return redirect("manage_companies")

    return render(request, "companies/create_company.html")

@login_required
@user_passes_test(is_tpo)
def manage_companies(request):
    companies = Company.objects.all()
    return render(request, "companies/manage_companies.html", {"companies": companies})

@login_required
def company_dashboard(request):
    if request.user.role != "COMPANY":
        return redirect("login")
    company = Company.objects.get(user=request.user)
    return render(request, "companies/company_dashboard.html", {"company": company})

@login_required
def complete_company_profile(request):
    company = get_object_or_404(Company, user=request.user)

    if request.method == "POST":
        # Basic Info
        company.name = request.POST.get("name")
        company.website = request.POST.get("website")
        company.industry_type = request.POST.get("industry_type")
        company.city = request.POST.get("city")
        company.address = request.POST.get("address")

        # HR Info
        company.hr_name = request.POST.get("hr_name")
        company.hr_email = request.POST.get("hr_email")
        company.hr_contact = request.POST.get("hr_contact")

        # Secondary Contacts
        company.secondary_contact_email = request.POST.get("secondary_contact_email")
        company.secondary_contact_number = request.POST.get("secondary_contact_number")

        # Descriptions
        company.technical_description = request.POST.get("technical_description")
        company.other_description = request.POST.get("other_description")

        # Preferences        
        company.hiring_types = request.POST.get("hiring_types")

        company.preferred_courses = request.POST.getlist("preferred_courses")
        

        # Mark as active if complete
        if company.is_complete():
            company.status = "ACTIVE"

        company.save()
        return redirect("company_dashboard")

    return render(request, "companies/complete_profile.html", {
        "company": company,
        "COURSE_CHOICES": COURSE_CHOICES
    })

@login_required
def company_dashboard(request):
    if request.user.role != "COMPANY":
        return redirect("login")

    company = get_object_or_404(Company, user=request.user)

    # If not complete → redirect to profile completion
    if company.status == "PENDING":
        return redirect("complete_company_profile")

    return render(request, "companies/company_dashboard.html", {"company": company})

@login_required
def create_job(request):
    if request.user.role != "COMPANY":
        return redirect("login")

    company = get_object_or_404(Company, user=request.user)

    if request.method == "POST":
        job = Job.objects.create(
            company=company,
            title=request.POST.get("title"),
            job_type=request.POST.get("job_type"),
            eligible_courses=request.POST.getlist("eligible_courses"),
            min_cgpa=request.POST.get("min_cgpa") or 0.0,
            max_backlogs=request.POST.get("max_backlogs") or 0,
            batch_year=request.POST.get("batch_year"),
            stipend=request.POST.get("stipend") or None,
            package=request.POST.get("package") or None,
            location=request.POST.get("location"),
            job_description=request.POST.get("job_description"),
            terms_conditions=request.POST.get("terms_conditions"),
            pdf_details=request.FILES.get("pdf_details"),
            application_deadline=request.POST.get("application_deadline"),
            drive_date=request.POST.get("drive_date") or None,
        )
        return redirect("company_dashboard")

    return render(request, "companies/create_job.html", {"COURSE_CHOICES": COURSE_CHOICES})


@login_required
def manage_jobs(request):
    if request.user.role != "COMPANY":
        return redirect("login")

    company = get_object_or_404(Company, user=request.user)
    jobs =  company.jobs.all()
    return render(request, "companies/manage_jobs.html", {"jobs": jobs})
