from django.db import models

# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)
    website = models.URLField(blank=True, null=True)
    industry_type = models.CharField(max_length=100, blank=True, null=True)  
    city = models.CharField(max_length=100)
    address = models.TextField()

    # HR / Contact Info
    hr_name = models.CharField(max_length=100, blank=True, null=True)
    hr_email = models.EmailField()
    hr_contact = models.CharField(max_length=15)

    # Additional Contacts (optional – for multiple rounds)
    secondary_contact_email = models.EmailField(blank=True, null=True)
    secondary_contact_number = models.CharField(max_length=15, blank=True, null=True)

    # Descriptions
    technical_description = models.TextField(blank=True, null=True)   # Tech stack, required skills
    other_description = models.TextField(blank=True, null=True)       # Culture, perks, general notes

    # Placement Preferences
    preferred_courses = models.CharField(max_length=255, blank=True, null=True)  
    hiring_types = models.CharField(max_length=50, choices=[
        ('INTERNSHIP', 'Internship'),
        ('FULLTIME', 'Full-time'),
        ('BOTH', 'Both'),
    ], default='FULLTIME')
    
    # Flags
    is_active = models.BooleanField(default=True)  # If company is still hiring / active partner

    # Audit
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class EligibleCourse(models.Model):
    name = models.CharField(max_length=50, unique=True)  # e.g., CS, IT, EC, MCA, MSIT

    def __str__(self):
        return self.name

class Job(models.Model):
    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='jobs')

    title = models.CharField(max_length=255)  # e.g., Software Engineer, QA Intern
    job_type = models.CharField(max_length=50, choices=[
        ('INTERNSHIP', 'Internship'),
        ('FULLTIME', 'Full-time'),
        ('BOTH', 'Both'),
    ], default='FULLTIME')

    # Eligibility
    eligible_courses = models.ManyToManyField('EligibleCourse')  # CS, IT, EC, MCA, etc.
    min_cgpa = models.DecimalField(max_digits=4, decimal_places=2, default=0.0)
    max_backlogs = models.IntegerField(default=0)
    batch_year = models.IntegerField()  # e.g., 2025 batch

    # Compensation
    stipend = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    package = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)

    # Details
    job_description = models.TextField()
    terms_conditions = models.TextField(blank=True, null=True)
    pdf_details = models.FileField(upload_to='job_pdfs/', blank=True, null=True)

    # Timeline
    application_deadline = models.DateField()
    drive_date = models.DateField(blank=True, null=True)

    # Status
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.company.name} - {self.title}"
