from django.core.management.base import BaseCommand
from django.utils import timezone
from placement.models import Company, JobApplication
from account.models import User
import random
from datetime import timedelta

class Command(BaseCommand):
    help = 'Generate dummy data for companies and students'

    def handle(self, *args, **options):
        # Create 30 students
        students = []
        for i in range(1, 31):
            user, created = User.objects.get_or_create(
                username=f'student{i}',
                defaults={
                    'email': f'student{i}@example.com',
                    'role': 'student',
                    'password': 'pbkdf2_sha256$260000$dummy$dummyhash'  # Set unusable password
                }
            )
            students.append(user)
        self.stdout.write(self.style.SUCCESS('Created 30 students'))

        # Create 25 companies
        company_types = ['Internship', 'Full-Time', 'Both']
        for i in range(1, 26):
            company, created = Company.objects.get_or_create(
                name=f'Company {i}',
                defaults={
                    'application_deadline': timezone.now().date() + timedelta(days=random.randint(1, 30)),
                    'company_type': random.choice(company_types),
                    'interview_date': timezone.now().date() + timedelta(days=random.randint(1, 30)),
                    'stipend': f'{random.randint(5000, 20000)} INR',
                    'package': f'{random.randint(3, 15)} LPA',
                    'address': f'Address {i}',
                    'position_details': f'Position details for Company {i}',
                    'required_skills': 'Python, Django, Communication',
                    'website_link': f'https://company{i}.com',
                    'linkedin_profile': f'https://linkedin.com/company{i}',
                    'pdf_link': '',
                    'extra_details': '',
                    'foundation_date': timezone.now().date() - timedelta(days=random.randint(1000, 10000)),
                    'owner_details': f'Owner {i}',
                    'company_work_details': f'Company {i} does amazing work.',
                }
            )
        self.stdout.write(self.style.SUCCESS('Created 25 companies'))

        # Create random job applications
        companies = Company.objects.all()
        for student in students:
            applied_companies = random.sample(list(companies), k=random.randint(5, 10))
            for company in applied_companies:
                JobApplication.objects.get_or_create(student=student, company=company)
        self.stdout.write(self.style.SUCCESS('Created job applications for students'))
