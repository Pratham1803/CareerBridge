from django.db import models
from django.conf import settings

class Company(models.Model):
    COMPANY_TYPE_CHOICES = [
        ('Internship', 'Internship'),
        ('Full-Time', 'Full-Time'),
        ('Both', 'Both'),
    ]

    name = models.CharField(max_length=100)
    application_deadline = models.DateField()
    company_type = models.CharField(max_length=20, choices=COMPANY_TYPE_CHOICES)

    interview_date = models.DateField(null=True, blank=True)  


    stipend = models.CharField(max_length=50, blank=True)
    package = models.CharField(max_length=50, blank=True)

    address = models.TextField(blank=True)
    position_details = models.TextField(help_text="Details about roles or positions")
    required_skills = models.TextField(help_text="Comma-separated skills")

    website_link = models.URLField(blank=True)
    linkedin_profile = models.URLField(blank=True)
    pdf_link = models.URLField(blank=True, help_text="Google Drive PDF link")

    extra_details = models.TextField(blank=True)
    foundation_date = models.DateField(null=True, blank=True)
    owner_details = models.CharField(max_length=200, blank=True)
    company_work_details = models.TextField(help_text="Overview of what the company does")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



class JobApplication(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    date_applied = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'company')  # prevent duplicate applications

    def __str__(self):
        return f"{self.student.username} → {self.company.name}"


# New model to store selected students for companies
class Selection(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    selected_on = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(blank=True)

    class Meta:
        unique_together = ('student', 'company')

    def __str__(self):
        return f"{self.student.username} selected for {self.company.name}"