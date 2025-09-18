from django.db import models

# Create your models here.
class Application(models.Model):
    student = models.ForeignKey('students.StudentProfile', on_delete=models.CASCADE)
    job = models.ForeignKey('companies.Job', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[
        ('APPLIED', 'Applied'),
        ('SHORTLISTED', 'Shortlisted'),
        ('INTERVIEW', 'Interview'),
        ('OFFERED', 'Offered'),
        ('REJECTED', 'Rejected'),
        ('PLACED', 'Placed'),
    ], default='APPLIED')
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.student_id} → {self.job.title} ({self.status})"
