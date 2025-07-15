from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from placement.models import Company, JobApplication
from django.template.loader import render_to_string
from django.utils.html import strip_tags


class Command(BaseCommand):
    help = 'Send interview reminder emails to students 2 days before their interview'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what emails would be sent without actually sending them',
        )

    def handle(self, *args, **options):
        # Calculate the target date (2 days from now)
        target_date = timezone.now().date() + timedelta(days=2)
        
        self.stdout.write(
            self.style.SUCCESS(f'Looking for interviews scheduled for: {target_date}')
        )

        # Find companies with interviews scheduled for the target date
        companies_with_interviews = Company.objects.filter(
            interview_date=target_date
        )

        if not companies_with_interviews.exists():
            self.stdout.write(
                self.style.WARNING(f'No interviews found for {target_date}')
            )
            return

        total_emails_sent = 0
        
        for company in companies_with_interviews:
            # Get all students who have applied to this company
            applications = JobApplication.objects.filter(
                company=company
            ).select_related('student')

            if not applications.exists():
                self.stdout.write(
                    self.style.WARNING(f'No applications found for {company.name}')
                )
                continue

            self.stdout.write(
                self.style.SUCCESS(f'Processing {company.name} - {applications.count()} students')
            )

            for application in applications:
                student = application.student
                
                if not student.email:
                    self.stdout.write(
                        self.style.WARNING(f'No email found for student: {student.username}')
                    )
                    continue

                # Prepare email context
                context = {
                    'student_name': student.first_name or student.username,
                    'company_name': company.name,
                    'interview_date': company.interview_date,
                    'company_address': company.address,
                    'company_type': company.company_type,
                    'position_details': company.position_details,
                    'required_skills': company.required_skills,
                    'package': company.package,
                    'website_link': company.website_link,
                    'linkedin_profile': company.linkedin_profile,
                }

                if options['dry_run']:
                    self.stdout.write(
                        f'  [DRY RUN] Would send email to: {student.email} ({student.username})'
                    )
                    continue

                try:
                    # Create email content
                    subject = f'Interview Reminder: {company.name} - {company.interview_date}'
                    
                    # HTML email content
                    html_message = f'''
                    <html>
                    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; text-align: center; margin-bottom: 20px;">
                                <h1 style="margin: 0; font-size: 24px;">🎯 Interview Reminder</h1>
                                <p style="margin: 10px 0 0 0; font-size: 16px;">CareerBridge Placement Portal</p>
                            </div>
                            
                            <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
                                <p style="margin: 0 0 15px 0; font-size: 18px;"><strong>Hello {context['student_name']},</strong></p>
                                <p style="margin: 0 0 15px 0;">This is a friendly reminder that you have an interview scheduled in <strong>2 days</strong>!</p>
                            </div>

                            <div style="background: white; border: 2px solid #e9ecef; border-radius: 8px; padding: 20px; margin-bottom: 20px;">
                                <h2 style="color: #495057; margin: 0 0 15px 0; font-size: 20px;">📋 Interview Details</h2>
                                <table style="width: 100%; border-collapse: collapse;">
                                    <tr style="border-bottom: 1px solid #e9ecef;">
                                        <td style="padding: 8px 0; font-weight: bold; width: 30%;">🏢 Company:</td>
                                        <td style="padding: 8px 0;">{context['company_name']}</td>
                                    </tr>
                                    <tr style="border-bottom: 1px solid #e9ecef;">
                                        <td style="padding: 8px 0; font-weight: bold;">📅 Date:</td>
                                        <td style="padding: 8px 0; color: #dc3545; font-weight: bold;">{context['interview_date']}</td>
                                    </tr>
                                    <tr style="border-bottom: 1px solid #e9ecef;">
                                        <td style="padding: 8px 0; font-weight: bold;">💼 Type:</td>
                                        <td style="padding: 8px 0;">{context['company_type']}</td>
                                    </tr>
                                    {'<tr style="border-bottom: 1px solid #e9ecef;"><td style="padding: 8px 0; font-weight: bold;">📍 Location:</td><td style="padding: 8px 0;">' + (context['company_address'] or 'TBD') + '</td></tr>' if context['company_address'] else ''}
                                    {'<tr style="border-bottom: 1px solid #e9ecef;"><td style="padding: 8px 0; font-weight: bold;">💰 Package:</td><td style="padding: 8px 0; color: #28a745; font-weight: bold;">' + (context['package'] or 'TBD') + '</td></tr>' if context['package'] else ''}
                                </table>
                            </div>

                            {'<div style="background: #fff3cd; border: 1px solid #ffeaa7; border-radius: 8px; padding: 15px; margin-bottom: 20px;"><h3 style="color: #856404; margin: 0 0 10px 0;">📝 Position Details:</h3><p style="margin: 0; color: #856404;">' + context['position_details'] + '</p></div>' if context['position_details'] else ''}

                            {'<div style="background: #d1ecf1; border: 1px solid #bee5eb; border-radius: 8px; padding: 15px; margin-bottom: 20px;"><h3 style="color: #0c5460; margin: 0 0 10px 0;">🛠️ Required Skills:</h3><p style="margin: 0; color: #0c5460;">' + context['required_skills'] + '</p></div>' if context['required_skills'] else ''}

                            <div style="background: #d4edda; border: 1px solid #c3e6cb; border-radius: 8px; padding: 20px; margin-bottom: 20px;">
                                <h3 style="color: #155724; margin: 0 0 15px 0;">💡 Preparation Tips:</h3>
                                <ul style="margin: 0; padding-left: 20px; color: #155724;">
                                    <li>Review your resume and be ready to discuss your projects</li>
                                    <li>Research the company background and recent news</li>
                                    <li>Prepare questions about the role and company culture</li>
                                    <li>Practice common interview questions</li>
                                    <li>Ensure you have proper interview attire ready</li>
                                    <li>Plan your route and arrive 10-15 minutes early</li>
                                </ul>
                            </div>

                            <div style="text-align: center; margin-bottom: 20px;">
                                {'<a href="' + context['website_link'] + '" style="display: inline-block; background: #007bff; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; margin: 5px;">🌐 Company Website</a>' if context['website_link'] else ''}
                                {'<a href="' + context['linkedin_profile'] + '" style="display: inline-block; background: #0077b5; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; margin: 5px;">💼 LinkedIn Profile</a>' if context['linkedin_profile'] else ''}
                            </div>

                            <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; text-align: center;">
                                <p style="margin: 0 0 10px 0; color: #6c757d;">Best of luck with your interview!</p>
                                <p style="margin: 0; color: #6c757d; font-size: 14px;">
                                    <strong>CareerBridge Team</strong><br>
                                    Placement Portal
                                </p>
                            </div>
                        </div>
                    </body>
                    </html>
                    '''

                    # Plain text version
                    plain_message = f'''
Interview Reminder - CareerBridge

Hello {context['student_name']},

This is a friendly reminder that you have an interview scheduled in 2 days!

Interview Details:
• Company: {context['company_name']}
• Date: {context['interview_date']}
• Type: {context['company_type']}
• Location: {context['company_address'] or 'TBD'}
• Package: {context['package'] or 'TBD'}

Position Details: {context['position_details'] or 'N/A'}

Required Skills: {context['required_skills'] or 'N/A'}

Preparation Tips:
- Review your resume and be ready to discuss your projects
- Research the company background and recent news
- Prepare questions about the role and company culture
- Practice common interview questions
- Ensure you have proper interview attire ready
- Plan your route and arrive 10-15 minutes early

Company Links:
• Website: {context['website_link'] or 'N/A'}
• LinkedIn: {context['linkedin_profile'] or 'N/A'}

Best of luck with your interview!

CareerBridge Team
Placement Portal
                    '''

                    # Send email
                    send_mail(
                        subject=subject,
                        message=plain_message,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[student.email],
                        html_message=html_message,
                        fail_silently=False,
                    )

                    total_emails_sent += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'  ✓ Email sent to: {student.email} ({student.username})')
                    )

                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'  ✗ Failed to send email to {student.email}: {str(e)}')
                    )

        if options['dry_run']:
            self.stdout.write(
                self.style.SUCCESS(f'\n[DRY RUN] Would have sent {total_emails_sent} emails')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f'\n✅ Successfully sent {total_emails_sent} interview reminder emails!')
            )
