from django.shortcuts import render, redirect, get_object_or_404
from .models import Company, JobApplication
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Case, When, Value, IntegerField
import openpyxl
from django.http import HttpResponse
from account.views import student_required

@login_required
def export_companies_excel(request):
    """Export companies to Excel"""
    query = request.GET.get('q', '')

    companies = Company.objects.all().order_by('-application_deadline')
    if query:
        companies = companies.filter(
            Q(name__icontains=query) |
            Q(required_skills__icontains=query) |
            Q(address__icontains=query)
        )

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Companies"

    ws.append([
        "Name", "Type", "Deadline", "Stipend", "Package", "Location", "Skills", "Interview Date"
    ])

    for c in companies:
        ws.append([
            c.name, c.company_type, c.application_deadline, c.stipend,
            c.package, c.address, c.required_skills, c.interview_date
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response['Content-Disposition'] = 'attachment; filename=companies.xlsx'
    wb.save(response)
    
    return response

@login_required
def export_applied_jobs_excel(request):
    query = request.GET.get('q', '')
    sort_by = request.GET.get('sort', 'date_applied')

    apps = JobApplication.objects.filter(student=request.user).select_related('company')
    if query:
        apps = apps.filter(
            Q(company__name__icontains=query) |
            Q(company__required_skills__icontains=query) |
            Q(company__address__icontains=query)
        )

    # Apply same sorting as in applied_jobs view
    if sort_by == 'interview_date':
        apps = apps.order_by(
            Case(
                When(company__interview_date__isnull=True, then=Value(1)),
                default=Value(0),
                output_field=IntegerField()
            ),
            'company__interview_date',
            '-date_applied'
        )
    elif sort_by == 'location':
        apps = apps.order_by('company__address', '-date_applied')
    else:  # Default: sort by date_applied
        apps = apps.order_by('-date_applied')

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Applied Companies"

    ws.append([
        "Company Name", "Applied On", "Type", "Deadline", "Stipend", "Package", "Location", "Interview Date"
    ])

    for app in apps:
        c = app.company
        ws.append([
            c.name, app.date_applied.strftime("%Y-%m-%d"), c.company_type,
            c.application_deadline, c.stipend, c.package, c.address, c.interview_date
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response['Content-Disposition'] = 'attachment; filename=applied_companies.xlsx'
    wb.save(response)
    return response


@login_required
@student_required
def company_list(request):
    """Display list of companies with search functionality"""
    query = request.GET.get('q', '')

    # Default: newest first
    companies = Company.objects.all().order_by('-application_deadline')

    if query:
        companies = companies.filter(
            Q(name__icontains=query) |
            Q(required_skills__icontains=query) |
            Q(address__icontains=query)
        )

    applied_company_ids = JobApplication.objects.filter(student=request.user).values_list('company_id', flat=True)

    return render(request, 'placement/company_list.html', {
        'companies': companies,
        'applied_company_ids': applied_company_ids,
        'query': query,
    })

@login_required
def apply_to_company(request, pk):
    """Apply to a company"""
    company = get_object_or_404(Company, pk=pk)

    # Prevent duplicate application
    already_applied = JobApplication.objects.filter(student=request.user, company=company).exists()
    if already_applied:
        messages.warning(request, 'You have already applied to this company.')
    else:
        JobApplication.objects.create(student=request.user, company=company)
        messages.success(request, 'Application submitted successfully.')

    return redirect('company_list')

@login_required
def applied_jobs(request):
    """View applied jobs with search and sorting"""
    query = request.GET.get('q', '')
    sort_by = request.GET.get('sort', 'date_applied')  # Default sort by application date

    applications = JobApplication.objects.filter(student=request.user).select_related('company')

    if query:
        applications = applications.filter(
            Q(company__name__icontains=query) |
            Q(company__required_skills__icontains=query) |
            Q(company__address__icontains=query)
        )

    # Apply sorting
    if sort_by == 'interview_date':
        # Sort by interview date (companies with interview dates first, then by date_applied)
        applications = applications.order_by(
            Case(
                When(company__interview_date__isnull=True, then=Value(1)),
                default=Value(0),
                output_field=IntegerField()
            ),
            'company__interview_date',
            '-date_applied'
        )
    elif sort_by == 'location':
        applications = applications.order_by('company__address', '-date_applied')
    else:  # Default: sort by date_applied
        applications = applications.order_by('-date_applied')

    return render(request, 'placement/applied_jobs.html', {
        'applications': applications,
        'query': query,
        'sort_by': sort_by
    })

@login_required
def company_detail(request, pk):
    """View company details"""
    company = get_object_or_404(Company, pk=pk)
    already_applied = JobApplication.objects.filter(student=request.user, company=company).exists()
    
    return render(request, 'placement/company_detail.html', {
        'company': company,
        'already_applied': already_applied
    })

@login_required
def withdraw_application(request, application_id):
    """Withdraw job application"""
    application = get_object_or_404(JobApplication, id=application_id, student=request.user)
    
    application.delete()
    messages.success(request, "Application withdrawn successfully.")
    
    return redirect('applied_jobs')