from django.contrib import admin
from django.utils import timezone
from datetime import timedelta
from .models import Company, JobApplication, Selection


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'company_type', 'application_deadline', 'interview_date', 'get_reminder_status']
    list_filter = ['company_type', 'application_deadline', 'interview_date']
    search_fields = ['name', 'address', 'required_skills']
    date_hierarchy = 'interview_date'
    ordering = ['interview_date', 'application_deadline']

    def get_reminder_status(self, obj):
        """Show reminder status for interviews"""
        if not obj.interview_date:
            return "No interview date"
        
        today = timezone.now().date()
        days_until_interview = (obj.interview_date - today).days
        
        if days_until_interview == 2:
            return "🔔 Reminder due today!"
        elif days_until_interview == 1:
            return "⚠️ Interview tomorrow"
        elif days_until_interview == 0:
            return "📅 Interview today"
        elif days_until_interview < 0:
            return "✅ Interview completed"
        elif days_until_interview <= 7:
            return f"📍 In {days_until_interview} days"
        else:
            return f"📆 In {days_until_interview} days"
    
    get_reminder_status.short_description = "Reminder Status"



@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ['student', 'company', 'date_applied', 'get_interview_date']
    list_filter = ['date_applied', 'company__company_type', 'company__interview_date']
    search_fields = ['student__username', 'student__email', 'company__name']
    date_hierarchy = 'date_applied'
    
    def get_interview_date(self, obj):
        """Show interview date for this application"""
        if obj.company.interview_date:
            return obj.company.interview_date
        return "No interview date"
    
    get_interview_date.short_description = "Interview Date"

# Register Selection model
@admin.register(Selection)
class SelectionAdmin(admin.ModelAdmin):
    list_display = ['student', 'company', 'selected_on', 'remarks']
    list_filter = ['selected_on', 'company__company_type']
    search_fields = ['student__username', 'company__name']