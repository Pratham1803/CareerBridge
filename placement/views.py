from django.shortcuts import render, redirect, get_object_or_404
from .models import Company, JobApplication
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.db.models import Q

import openpyxl
from django.http import HttpResponse

@login_required
def export_companies_excel(request):
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

    apps = JobApplication.objects.filter(student=request.user).select_related('company').order_by('-applied_at')
    if query:
        apps = apps.filter(
            Q(company__name__icontains=query) |
            Q(company__required_skills__icontains=query) |
            Q(company__address__icontains=query)
        )

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Applied Companies"

    ws.append([
        "Company Name", "Applied On", "Type", "Deadline", "Stipend", "Package", "Location", "Interview Date"
    ])

    for app in apps:
        c = app.company
        ws.append([
            c.name, app.applied_at.strftime("%Y-%m-%d"), c.company_type,
            c.application_deadline, c.stipend, c.package, c.address, c.interview_date
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response['Content-Disposition'] = 'attachment; filename=applied_companies.xlsx'
    wb.save(response)
    return response


@login_required
def company_list(request):
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
    query = request.GET.get('q', '')

    applications = JobApplication.objects.filter(student=request.user).select_related('company')

    if query:
        applications = applications.filter(
            Q(company__name__icontains=query) |
            Q(company__required_skills__icontains=query) |
            Q(company__address__icontains=query)
        )

    applications = applications.order_by('-date_applied')

    return render(request, 'placement/applied_jobs.html', {
        'applications': applications,
        'query': query
    })

@login_required
def company_detail(request, pk):
    company = get_object_or_404(Company, pk=pk)
    already_applied = JobApplication.objects.filter(student=request.user, company=company).exists()
    return render(request, 'placement/company_detail.html', {
        'company': company,
        'already_applied': already_applied
    })

@login_required
def withdraw_application(request, application_id):
    application = get_object_or_404(JobApplication, id=application_id, student=request.user)
    application.delete()
    messages.success(request, "Application withdrawn successfully.")
    return redirect('applied_jobs')
