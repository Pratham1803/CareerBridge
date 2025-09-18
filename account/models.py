from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('TPO', 'Training & Placement Officer'),
        ('STUDENT', 'Student'),
        ('COMPANY', 'Company HR'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='STUDENT')

    def is_tpo(self):
        return self.role == 'TPO'

    def is_company(self):
        return self.role == 'COMPANY'

    def is_student(self):
        return self.role == 'STUDENT'
