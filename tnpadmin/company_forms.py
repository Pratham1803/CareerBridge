from django import forms
from placement.models import Company

class AdminCompanyForm(forms.ModelForm):
    cgpa_criteria = forms.DecimalField(label='Minimum CGPA', required=False)
    eligible_branches = forms.CharField(label='Eligible Branches (comma separated)', required=False)
    class Meta:
        model = Company
        fields = ['name', 'application_deadline', 'company_type', 'interview_date', 'stipend', 'package', 'address', 'position_details', 'required_skills', 'website_link', 'linkedin_profile', 'pdf_link', 'extra_details', 'foundation_date', 'owner_details', 'company_work_details']
