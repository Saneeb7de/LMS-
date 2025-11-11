from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from courses.models import Course, Module, Enrollment
from courses.forms import CourseForm, ModuleForm
from accounts.models import User
from payments.models import Payment
from django.db.models import Count, Sum, Q
import csv
from datetime import datetime, timedelta

@login_required
def admin_course_list(request):
    if not request.user.is_admin_user:
        messages.error(request, 'Access denied. Admin only.')
        return redirect('user_dashboard')
    
    courses = Course.objects.all().annotate(
        enrollment_count=Count('enrollments')
    ).order_by('-created_at')
    
    context = {
        'courses': courses
    }
    
    return render(request, 'courses/admin_course_list.html', context)

@login_required
def admin_course_create(request):
    if not request.user.is_admin_user:
        messages.error(request, 'Access denied. Admin only.')
        return redirect('user_dashboard')
    
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.created_by = request.user
            course.save()
            messages.success(request, 'Course created successfully!')
            return redirect('admin_course_edit', course_id=course.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CourseForm()
    
    context = {
        'form': form,
        'is_edit': False
    }
    
    return render(request, 'courses/admin_course_form.html', context)

@login_required
def admin_course_edit(request, course_id):
    if not request.user.is_admin_user:
        messages.error(request, 'Access denied. Admin only.')
        return redirect('user_dashboard')
    
    course = get_object_or_404(Course, id=course_id)
    modules = course.modules.all()
    
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course updated successfully!')
            return redirect('admin_course_edit', course_id=course.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CourseForm(instance=course)
    
    context = {
        'form': form,
        'course': course,
        'modules': modules,
        'is_edit': True
    }
    
    return render(request, 'courses/admin_course_form.html', context)

@login_required
def admin_course_delete(request, course_id):
    if not request.user.is_admin_user:
        return JsonResponse({'success': False, 'message': 'Access denied'})
    
    if request.method == 'POST':
        course = get_object_or_404(Course, id=course_id)
        course_title = course.title
        course.delete()
        return JsonResponse({'success': True, 'message': f'Course "{course_title}" deleted successfully'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})

@login_required
def admin_module_create(request, course_id):
    if not request.user.is_admin_user:
        messages.error(request, 'Access denied. Admin only.')
        return redirect('user_dashboard')
    
    course = get_object_or_404(Course, id=course_id)
    
    if request.method == 'POST':
        form = ModuleForm(request.POST, request.FILES)
        if form.is_valid():
            module = form.save(commit=False)
            module.course = course
            module.save()
            messages.success(request, 'Module added successfully!')
            return redirect('admin_course_edit', course_id=course.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        # Set default order to last
        next_order = course.modules.count() + 1
        form = ModuleForm(initial={'order': next_order})
    
    context = {
        'form': form,
        'course': course,
        'is_edit': False
    }
    
    return render(request, 'courses/admin_module_form.html', context)

@login_required
def admin_module_edit(request, module_id):
    if not request.user.is_admin_user:
        messages.error(request, 'Access denied. Admin only.')
        return redirect('user_dashboard')
    
    module = get_object_or_404(Module, id=module_id)
    
    if request.method == 'POST':
        form = ModuleForm(request.POST, request.FILES, instance=module)
        if form.is_valid():
            form.save()
            messages.success(request, 'Module updated successfully!')
            return redirect('admin_course_edit', course_id=module.course.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ModuleForm(instance=module)
    
    context = {
        'form': form,
        'module': module,
        'course': module.course,
        'is_edit': True
    }
    
    return render(request, 'courses/admin_module_form.html', context)

@login_required
def admin_module_delete(request, module_id):
    if not request.user.is_admin_user:
        return JsonResponse({'success': False, 'message': 'Access denied'})
    
    if request.method == 'POST':
        module = get_object_or_404(Module, id=module_id)
        course_id = module.course.id
        module_title = module.title
        module.delete()
        return JsonResponse({
            'success': True, 
            'message': f'Module "{module_title}" deleted successfully',
            'course_id': course_id
        })
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})

@login_required
def admin_analytics(request):
    if not request.user.is_admin_user:
        messages.error(request, 'Access denied. Admin only.')
        return redirect('user_dashboard')
    
    # Get date range from request or default to last 30 days
    days = int(request.GET.get('days', 30))
    start_date = datetime.now() - timedelta(days=days)
    
    # Statistics
    total_courses = Course.objects.count()
    total_users = User.objects.filter(user_type='student').count()
    total_enrollments = Enrollment.objects.count()
    active_enrollments = Enrollment.objects.filter(is_active=True).count()
    
    total_revenue = Payment.objects.filter(
        payment_status='completed'
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    recent_revenue = Payment.objects.filter(
        payment_status='completed',
        transaction_date__gte=start_date
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    # Top courses by enrollment
    top_courses = Course.objects.annotate(
        enrollment_count=Count('enrollments')
    ).order_by('-enrollment_count')[:5]
    
    # Recent enrollments
    recent_enrollments = Enrollment.objects.select_related(
        'user', 'course'
    ).order_by('-enrolled_at')[:10]
    
    # All users for management
    users = User.objects.filter(user_type='student').annotate(
        enrollment_count=Count('enrollments')
    ).order_by('-date_joined')
    
    # Recent payments
    recent_payments = Payment.objects.select_related(
        'user', 'course'
    ).order_by('-transaction_date')[:10]
    
    context = {
        'total_courses': total_courses,
        'total_users': total_users,
        'total_enrollments': total_enrollments,
        'active_enrollments': active_enrollments,
        'total_revenue': total_revenue,
        'recent_revenue': recent_revenue,
        'top_courses': top_courses,
        'recent_enrollments': recent_enrollments,
        'users': users,
        'recent_payments': recent_payments,
        'days': days,
    }
    
    return render(request, 'courses/admin_analytics.html', context)

@login_required
def export_data_csv(request):
    if not request.user.is_admin_user:
        messages.error(request, 'Access denied. Admin only.')
        return redirect('user_dashboard')
    
    # Create the HttpResponse object with CSV header
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="lms_data_{datetime.now().strftime("%Y%m%d")}.csv"'
    
    writer = csv.writer(response)
    
    # Courses data
    writer.writerow(['COURSES'])
    writer.writerow(['ID', 'Title', 'Type', 'Price', 'Enrollments', 'Created By', 'Created At'])
    courses = Course.objects.annotate(enrollment_count=Count('enrollments'))
    for course in courses:
        writer.writerow([
            course.id,
            course.title,
            course.course_type,
            course.price,
            course.enrollment_count,
            course.created_by.username,
            course.created_at.strftime('%Y-%m-%d %H:%M')
        ])
    
    writer.writerow([])
    
    # Enrollments data
    writer.writerow(['ENROLLMENTS'])
    writer.writerow(['ID', 'User', 'Course', 'Enrolled At', 'Progress', 'Status'])
    enrollments = Enrollment.objects.select_related('user', 'course')
    for enrollment in enrollments:
        writer.writerow([
            enrollment.id,
            enrollment.user.username,
            enrollment.course.title,
            enrollment.enrolled_at.strftime('%Y-%m-%d %H:%M'),
            f"{enrollment.progress}%",
            'Active' if enrollment.is_active else 'Inactive'
        ])
    
    writer.writerow([])
    
    # Payments data
    writer.writerow(['PAYMENTS'])
    writer.writerow(['ID', 'User', 'Course', 'Amount', 'Status', 'Transaction Date'])
    payments = Payment.objects.select_related('user', 'course')
    for payment in payments:
        writer.writerow([
            payment.id,
            payment.user.username,
            payment.course.title,
            payment.amount,
            payment.payment_status,
            payment.transaction_date.strftime('%Y-%m-%d %H:%M')
        ])
    
    return response
