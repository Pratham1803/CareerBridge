# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import StudentRegistrationForm, StudentProfileForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from .models import User, StudentProfile

def student_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 'student':
            return redirect('admin_dashboard')  # Redirect to admin dashboard if not a student
            # return HttpResponseForbidden("You do not have permission to access this page.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

@login_required
@student_required
def student_dashboard(request):
    """Student dashboard with dynamic stats and activity"""
    from placement.models import JobApplication, Company, Selection
    user = request.user
    # Applications sent
    applications_count = JobApplication.objects.filter(student=user).count()
    # Upcoming interviews
    upcoming_interviews = JobApplication.objects.filter(student=user, company__interview_date__gte=user.date_joined).order_by('company__interview_date')
    upcoming_count = upcoming_interviews.count()
    # Pending responses (applications without selection)
    pending_count = JobApplication.objects.filter(student=user).exclude(company__selection__student=user).count()
    # Success rate (selected/applications)
    selected_count = Selection.objects.filter(student=user).count()
    success_rate = int((selected_count / applications_count) * 100) if applications_count else 0
    # Recent activity (last 5 applications)
    recent_apps = JobApplication.objects.filter(student=user).order_by('-date_applied')[:5]
    # Upcoming deadlines (next 5 companies)
    upcoming_deadlines = Company.objects.filter(application_deadline__gte=user.date_joined).order_by('application_deadline')[:5]

    return render(request, 'accounts/student_dashboard.html', {
        'applications_count': applications_count,
        'upcoming_count': upcoming_count,
        'pending_count': pending_count,
        'success_rate': success_rate,
        'recent_apps': recent_apps,
        'upcoming_deadlines': upcoming_deadlines,
    })

def register_student(request):
    """Student registration with profile creation"""
    if request.method == 'POST':
        user_form = StudentRegistrationForm(request.POST)
        profile_form = StudentProfileForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            try:
                # Create user
                user = User.objects.create_user(
                    username=profile_form.cleaned_data['student_id'],  # Use student_id as username
                    email=user_form.cleaned_data['email'],
                    password=user_form.cleaned_data['password1']
                )
                user.role = 'student'
                user.first_name = profile_form.cleaned_data['first_name']
                user.last_name = profile_form.cleaned_data['last_name']
                user.save()

                # Create profile and assign all fields
                profile = StudentProfile(
                    user=user,
                    first_name=profile_form.cleaned_data['first_name'],
                    last_name=profile_form.cleaned_data['last_name'],
                    student_id=profile_form.cleaned_data['student_id'],
                    contact_number=profile_form.cleaned_data['contact_number'],
                    program=profile_form.cleaned_data['program'],
                    branch=profile_form.cleaned_data['branch'],
                    gender=profile_form.cleaned_data['gender'],
                    city=profile_form.cleaned_data['city'],
                    address=profile_form.cleaned_data['address'],
                    cgpa=profile_form.cleaned_data['cgpa']
                )
                profile.save()

                # Log the user in
                login(request, user)
                messages.success(request, 'Registration successful! Welcome to CareerBridge.')
                return redirect('student_home')
            
            except Exception as e:
                messages.error(request, f'An error occurred during registration: {str(e)}')
                # If there was an error, delete the user if it was created
                if 'user' in locals():
                    user.delete()
    else:
        user_form = StudentRegistrationForm()
        profile_form = StudentProfileForm()
    
    return render(request, 'accounts/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

def login_view(request):
    """Login view"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            if user.role == 'student':
                return redirect('student_home')
            else:
                return redirect('/tnp')
    else:
        form = AuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def logout_view(request):
    """Logout view"""
    logout(request)
    return redirect('login')

@login_required
@student_required
def student_profile(request):
    """Profile view"""
    return render(request, 'accounts/profile.html')