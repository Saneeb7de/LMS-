from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q, Sum
from .forms import AdminLoginForm, UserLoginForm, UserRegistrationForm
from .models import User
from courses.models import Course, Enrollment
from payments.models import Payment
import csv
from django.http import HttpResponse
from datetime import datetime, timedelta

# Admin Login View
def admin_login(request):
    if request.user.is_authenticated and request.user.is_admin_user:
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        form = AdminLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None and user.is_admin_user:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('admin_dashboard')
            else:
                messages.error(request, 'Invalid admin credentials or you do not have admin access.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AdminLoginForm()
    
    return render(request, 'accounts/admin_login.html', {'form': form})

# Admin Dashboard View
@login_required
def admin_dashboard(request):
    if not request.user.is_admin_user:
        messages.error(request, 'Access denied. Admin only.')
        return redirect('user_dashboard')
    
    # Get statistics
    total_courses = Course.objects.count()
    total_users = User.objects.filter(user_type='student').count()
    total_enrollments = Enrollment.objects.count()
    total_revenue = Payment.objects.filter(payment_status='completed').aggregate(
        total=Sum('amount')
    )['total'] or 0
    
    # Get recent courses
    recent_courses = Course.objects.all()[:5]
    
    context = {
        'total_courses': total_courses,
        'total_users': total_users,
        'total_enrollments': total_enrollments,
        'total_revenue': total_revenue,
        'recent_courses': recent_courses,
    }
    
    return render(request, 'accounts/admin_dashboard.html', context)

# User Login View
def user_login(request):
    if request.user.is_authenticated:
        return redirect('user_dashboard')
    
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            remember_me = form.cleaned_data.get('remember_me')
            
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                if not remember_me:
                    request.session.set_expiry(0)
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('user_dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid form submission.')
    else:
        form = UserLoginForm()
    
    return render(request, 'accounts/user_login.html', {'form': form})

# User Registration View
def user_register(request):
    if request.user.is_authenticated:
        return redirect('user_dashboard')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'student'
            user.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to the LMS Platform.')
            return redirect('user_dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/user_register.html', {'form': form})

# Logout View
@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('user_login')
