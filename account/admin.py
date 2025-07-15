from django.contrib import admin
from .models import User, StudentProfile

# Register your models here.
admin.site.register(User)
@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'student_id', 'program', 'branch')
    search_fields = ('user__username', 'first_name', 'last_name', 'student_id')
    list_filter = ('program', 'branch')
    ordering = ('user__username',)
    
    def get_queryset(self, request):
        """Optimize queryset to include related user data"""
        return super().get_queryset(request).select_related('user')