from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.admin.views.decorators import staff_member_required
from django.core.management import call_command
from django.utils import timezone
from datetime import timedelta
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from account.models import User
from placement.models import Company, JobApplication, Selection

@staff_member_required
def admin_toggle_selected(request, app_id):
    """Toggle selection status for a student's application to a company"""
    application = get_object_or_404(JobApplication, id=app_id)
    selection_exists = Selection.objects.filter(student=application.student, company=application.company).exists()
    if selection_exists:
        Selection.objects.filter(student=application.student, company=application.company).delete()
        messages.success(request, f"{application.student.username} deselected for {application.company.name}.")
    else:
        Selection.objects.create(student=application.student, company=application.company)
        messages.success(request, f"{application.student.username} selected for {application.company.name}.")
    return redirect('admin_selected_students')

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.management import call_command
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
import openpyxl
from django.http import HttpResponse
from account.models import User
from .forms import AdminUserForm
from .company_forms import AdminCompanyForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST

# Create your views here.
@staff_member_required
def send_interview_reminders_view(request):
    """Admin view to manually trigger interview reminder emails"""
    if request.method == 'POST':
        try:
            # Get the target date (2 days from now)
            target_date = timezone.now().date() + timedelta(days=2)
            
            # Check if this is a dry run
            dry_run = request.POST.get('dry_run') == 'on'
            
            if dry_run:
                # Capture output from management command
                from io import StringIO
                import sys
                
                old_stdout = sys.stdout
                sys.stdout = mystdout = StringIO()
                
                call_command('send_interview_reminders', '--dry-run')
                
                sys.stdout = old_stdout
                output = mystdout.getvalue()
                
                return JsonResponse({
                    'success': True,
                    'message': 'Dry run completed successfully',
                    'output': output,
                    'dry_run': True
                })
            else:
                # Actually send emails
                call_command('send_interview_reminders')
                messages.success(request, f'Interview reminder emails have been sent for interviews on {target_date}')
                return JsonResponse({
                    'success': True,
                    'message': 'Emails sent successfully',
                    'dry_run': False
                })
                
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    # GET request - show the form
    target_date = timezone.now().date() + timedelta(days=2)
    
    # Get companies with interviews on target date
    companies_with_interviews = Company.objects.filter(interview_date=target_date)
    
    # Get student counts for each company
    companies_data = []
    total_students = 0
    
    for company in companies_with_interviews:
        student_count = JobApplication.objects.filter(company=company).count()
        companies_data.append({
            'company': company,
            'student_count': student_count
        })
        total_students += student_count
    
    return render(request, 'placement/send_reminders.html', {
        'target_date': target_date,
        'companies_data': companies_data,
        'total_students': total_students,
    })

@staff_member_required
def admin_dashboard(request):
    return render(request, 'tnpadmin/admin_dashboard.html')

@staff_member_required
def admin_dashboard_stats(request):
    total_students = User.objects.filter(role='student').count()
    placed_students = JobApplication.objects.values('student').distinct().count()
    unplaced_students = total_students - placed_students
    # Get all departments from student profiles, fallback to empty list if none
    departments = User.objects.filter(role='student', profile__isnull=False).values_list('profile__program', flat=True).distinct()
    dept_stats = []
    for dept in departments:
        dept_total = User.objects.filter(role='student', profile__program=dept).count()
        dept_placed = JobApplication.objects.filter(student__profile__program=dept).values('student').distinct().count()
        dept_stats.append({'department': dept or 'N/A', 'total': dept_total, 'placed': dept_placed})
    # If no departments, add a default row
    if not dept_stats:
        dept_stats.append({'department': 'N/A', 'total': 0, 'placed': 0})
    return render(request, 'tnpadmin/admin_dashboard_stats.html', {
        'total_students': total_students or 0,
        'placed_students': placed_students or 0,
        'unplaced_students': unplaced_students or 0,
        'dept_stats': dept_stats,
    })

@staff_member_required
def admin_export_report_excel(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Placement Report"
    ws.append(["Student", "Email", "Department", "Company", "Date Applied"])
    applications = JobApplication.objects.select_related('student', 'company')
    for app in applications:
        ws.append([
            app.student.username,
            app.student.email,
            getattr(app.student.profile, 'program', '') if hasattr(app.student, 'profile') else '',
            app.company.name,
            app.date_applied.strftime("%Y-%m-%d")
        ])
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = 'attachment; filename=placement_report.xlsx'
    wb.save(response)
    return response

@staff_member_required
def admin_company_list(request):
    # Filters
    month = request.GET.get('month')
    location = request.GET.get('location')
    company_name = request.GET.get('company')
    companies = Company.objects.all()
    if month:
        companies = companies.filter(interview_date__month=month)
    if location:
        companies = companies.filter(address__icontains=location)
    if company_name:
        companies = companies.filter(name=company_name)
    months = Company.objects.dates('interview_date', 'month')
    locations = Company.objects.values_list('address', flat=True).distinct()
    return render(request, 'tnpadmin/admin_company_list.html', {
        'filtered_companies': companies,
        'months': months,
        'locations': locations,
        'companies': Company.objects.all(),
    })

@staff_member_required
def admin_student_list(request):
    company_name = request.GET.get('company')
    program = request.GET.get('program')
    students = User.objects.filter(role='student')
    if company_name:
        students = students.filter(jobapplication__company__name=company_name)
    if program:
        students = students.filter(profile__program=program) if hasattr(User, 'profile') else students
    companies = Company.objects.all()
    programs = students.values_list('profile__program', flat=True).distinct() if hasattr(User, 'profile') else []
    # Annotate students with applied and selected companies
    from placement.models import Selection
    for student in students:
        student.applied_companies = Company.objects.filter(jobapplication__student=student).distinct()
        student.selected_companies = Company.objects.filter(selection__student=student).distinct()
    return render(request, 'tnpadmin/admin_student_list.html', {
        'filtered_students': students,
        'companies': companies,
        'programs': programs,
    })

@staff_member_required
def admin_selected_students(request):
    company_name = request.GET.get('company')
    program = request.GET.get('program')

    # Get students who have at least one selected application
    from placement.models import Selection
    selected_students = User.objects.filter(
        role='student',
        selection__isnull=False
    ).distinct()

    if company_name:
        selected_students = selected_students.filter(
            selection__company__name=company_name
        )

    if program:
        # Filter manually since profile is a separate model
        selected_students = [s for s in selected_students if hasattr(s, 'profile') and s.profile.program == program]

    companies = Company.objects.all()
    programs = selected_students.values_list('profile__program', flat=True).distinct() if hasattr(User, 'profile') else []

    # Attach selected companies directly to each student
    for student in selected_students:
        student.selected_companies = Company.objects.filter(
            selection__student=student
        )

    return render(request, 'tnpadmin/admin_selected_students.html', {
        'selected_students': selected_students,
        'companies': companies,
        'programs': programs,
    })


@staff_member_required
def admin_user_management(request):
    query = request.GET.get('q', '')
    sort = request.GET.get('sort', 'username')
    users = User.objects.all()
    if query:
        users = users.filter(username__icontains=query)
    users = users.order_by(sort)
    paginator = Paginator(users, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'tnpadmin/admin_user_management.html', {'page_obj': page_obj, 'query': query, 'sort': sort})

@staff_member_required
def admin_user_create(request):
    if request.method == 'POST':
        form = AdminUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User created successfully.')
            return redirect('admin_user_management')
    else:
        form = AdminUserForm()
    return render(request, 'tnpadmin/admin_user_form.html', {'form': form, 'action': 'Create'})

@staff_member_required
def admin_user_edit(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = AdminUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully.')
            return redirect('admin_user_management')
    else:
        form = AdminUserForm(instance=user)
    return render(request, 'tnpadmin/admin_user_form.html', {'form': form, 'action': 'Edit'})

@staff_member_required
def admin_user_delete(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    messages.success(request, 'User deleted successfully.')
    return redirect('admin_user_management')

@staff_member_required
def admin_user_reset_password(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        if new_password:
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Password reset successfully.')
            return redirect('admin_user_management')
        else:
            messages.error(request, 'Please enter a new password.')
    return render(request, 'tnpadmin/admin_user_reset_password.html', {'user': user})

@staff_member_required
def admin_user_toggle_active(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = not user.is_active
    user.save()
    status = 'activated' if user.is_active else 'deactivated'
    messages.success(request, f'User {status} successfully.')
    return redirect('admin_user_management')

@staff_member_required
def admin_company_create(request):
    if request.method == 'POST':
        form = AdminCompanyForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Company created successfully.')
            return redirect('admin_company_list')
    else:
        form = AdminCompanyForm()
    return render(request, 'tnpadmin/admin_company_form.html', {'form': form, 'action': 'Create'})

@staff_member_required
def admin_company_edit(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    if request.method == 'POST':
        form = AdminCompanyForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            messages.success(request, 'Company updated successfully.')
            return redirect('admin_company_list')
    else:
        form = AdminCompanyForm(instance=company)
    return render(request, 'tnpadmin/admin_company_form.html', {'form': form, 'action': 'Edit'})

@staff_member_required
def admin_company_delete(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    company.delete()
    messages.success(request, 'Company deleted successfully.')
    return redirect('admin_company_list')

@staff_member_required
def admin_placement_tracking(request):
    companies = Company.objects.all()
    students = User.objects.filter(role='student')
    applied = JobApplication.objects.select_related('student', 'company')
    selected = applied.filter(company__interview_date__lte=timezone.now().date())  # Example: selected after interview
    return render(request, 'tnpadmin/admin_placement_tracking.html', {
        'companies': companies,
        'students': students,
        'applied': applied,
        'selected': selected,
    })

@staff_member_required
def admin_notify_students(request):
    companies = Company.objects.all()
    message = None
    if request.method == 'POST':
        company_id = request.POST.get('company_id')
        subject = request.POST.get('subject')
        body = request.POST.get('body')
        company = Company.objects.get(id=company_id)
        students = User.objects.filter(role='student')
        emails = students.values_list('email', flat=True)
        send_mail(subject, body, 'noreply@careerbridge.com', emails)
        message = f'Notification sent to {students.count()} students for {company.name}.'
    return render(request, 'tnpadmin/admin_notify_students.html', {'companies': companies, 'message': message})

@staff_member_required
def admin_report(request):
    company_id = request.GET.get('company')
    batch = request.GET.get('batch')
    year = request.GET.get('year')
    applications = JobApplication.objects.select_related('student', 'company')
    if company_id:
        applications = applications.filter(company_id=company_id)
    if batch:
        applications = applications.filter(student__profile__batch=batch) if hasattr(User, 'profile') else applications
    if year:
        applications = applications.filter(date_applied__year=year)
    companies = Company.objects.all()
    batches = User.objects.filter(role='student').values_list('profile__batch', flat=True).distinct() if hasattr(User, 'profile') else []
    years = applications.values_list('date_applied__year', flat=True).distinct()
    return render(request, 'tnpadmin/admin_report.html', {
        'applications': applications,
        'companies': companies,
        'batches': batches,
        'years': years,
    })

@staff_member_required
def admin_export_report_pdf(request):
    company_id = request.GET.get('company')
    batch = request.GET.get('batch')
    year = request.GET.get('year')
    applications = JobApplication.objects.select_related('student', 'company')
    if company_id:
        applications = applications.filter(company_id=company_id)
    if batch:
        applications = applications.filter(student__profile__batch=batch) if hasattr(User, 'profile') else applications
    if year:
        applications = applications.filter(date_applied__year=year)
    html = render_to_string('admin_report_pdf.html', {'applications': applications})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=placement_report.pdf'
    pisa.CreatePDF(html, dest=response)
    return response

@staff_member_required
def admin_profile(request):
    return render(request, 'accounts/admin_profile.html')

def select_student_for_company(request, app_id):
    from placement.models import Selection, JobApplication, Company

    app = get_object_or_404(JobApplication, id=app_id)
    student_id = app.student.id
    company_id = app.company.id
    student = User.objects.get(id=student_id)
    company = Company.objects.get(id=company_id)
    # Mark as selected
    Selection.objects.create(student=student, company=company)
    # Discard other applications
    JobApplication.objects.filter(student=student).exclude(company=company).delete()
    messages.success(request, f"{student.username} selected for {company.name}. Other applications discarded.")
    return redirect('admin_selected_students')
