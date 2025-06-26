# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import StudentRegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required


@login_required
def student_dashboard(request):
    return render(request, 'accounts/student_dashboard.html')


def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('company_list')
    else:
        form = StudentRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()  # ✅ this line is critical
            login(request, user)
            
            if user.role == 'student':
                return redirect('company_list')
            else:
                return redirect('/admin/')  # or some other admin dashboard
    else:
        form = AuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def student_profile(request):
    return render(request, 'accounts/profile.html')