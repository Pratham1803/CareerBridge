# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.username} ({self.role})"

# New model for storing more student details
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    student_id = models.CharField(max_length=20, unique=True)
    contact_number = models.CharField(max_length=15)
    program = models.CharField(max_length=100, choices=[
        ('B.Tech', 'Bachelor of Technology'),
        ('M.Tech', 'Master of Technology'),
        ('BCA', 'Bachelor of Computer Applications'),
        ('MCA', 'Master of Computer Applications'),
    ], default='B.Tech')
    branch = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    city = models.CharField(max_length=100)
    address = models.TextField()
    cgpa = models.DecimalField(max_digits=4, decimal_places=2)
    # Add more fields as needed

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"
