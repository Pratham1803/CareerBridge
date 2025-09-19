from django.db import models
# from django.contrib.auth.models import User

COURSE_CHOICES = [
    ("BTECH", "B.Tech"),
    ("MCA", "MCA"),
    ("MSIT", "MSIT"),
]


# Create your models here.
class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class StudentProfile(models.Model):
    user = models.OneToOneField("account.CustomUser", on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20, unique=True)

    # Personal Info
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=[
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
        ('OTHER', 'Other'),
    ])
    dob = models.DateField(null=True, blank=True)

    # Contact Info
    email_college = models.EmailField(unique=True)
    email_personal = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=15)
    city = models.CharField(max_length=100)
    permanent_address = models.TextField()

    # Academics
    tenth_percentage = models.DecimalField(max_digits=5, decimal_places=2, help_text="10th Grade Percentage", null=True, blank=True)
    twelfth_percentage = models.DecimalField(max_digits=5, decimal_places=2, help_text="12th Grade Percentage", null=True, blank=True)
    bachelor_college = models.CharField(max_length=255, null=True, blank=True)
    bachelor_course = models.CharField(max_length=50, choices=[
        ('CS', 'Computer Science'),
        ('IT', 'Information Technology'),
        ('EC', 'Electronics and Communication'),
        ('BCA', 'Bachelor of Computer Applications'),
        ('BScIT', 'Bachelor of Science in IT'),
        ('OTHER', 'Other'),
    ])
    bachelor_cgpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)

    master_college = models.CharField(max_length=255, blank=True, null=True)
    master_course = models.CharField(max_length=50, choices=[
        ('MCA', 'Master of Computer Applications'),
        ('MSIT', 'Master of Science in IT'),
        ('M.Tech', 'Master of Technology'),
        ('OTHER', 'Other'),
    ], blank=True, null=True)
    master_cgpa = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)

    # Extra Academic / Eligibility Info
    active_backlogs = models.IntegerField(default=0)
    batch_year = models.IntegerField(null=True, blank=True)

    # Skills
    skills = models.ManyToManyField(Skill, blank=True)

    # Online Profiles
    linkedin_url = models.URLField(blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    portfolio_url = models.URLField(blank=True, null=True)

    # Placement Info
    resume_link = models.URLField(max_length=500, null=True, blank=True)  # Only link, no file upload
    status = models.CharField(max_length=20, choices=[
        ('PENDING', 'Pending'),
        ('ACTIVE', 'Active'),
        ('PLACED', 'Placed'),
        ('INACTIVE', 'Inactive'),
    ], default='PENDING')
    can_apply = models.BooleanField(default=True)

    # Audit
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student_id} - {self.first_name} {self.last_name}"
