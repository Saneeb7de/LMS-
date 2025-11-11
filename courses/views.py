from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Count, Avg
from .models import Course, Module, Enrollment, ModuleProgress
from .forms import CourseForm, ModuleForm
from payments.models import Payment
from django.utils import timezone

# User Dashboard View
@login_required
def user_dashboard(request):
    # Get enrolled courses
    enrolled_courses = Enrollment.objects.filter(
        user=request.user, 
        is_active=True
    ).select_related('course')
    
    # Separate completed and in-progress courses
    completed_courses = enrolled_courses.filter(progress=100)
    in_progress_courses = enrolled_courses.filter(progress__lt=100)
    
    # Get all available courses
    all_courses = Course.objects.filter(is_active=True).annotate(
        enrollment_count=Count('enrollments')
    )
    
    # Recommendations (courses not enrolled)
    enrolled_course_ids = enrolled_courses.values_list('course_id', flat=True)
    recommended_courses = all_courses.exclude(id__in=enrolled_course_ids)[:6]
    
    context = {
        'enrolled_courses': enrolled_courses,
        'in_progress_courses': in_progress_courses,
        'completed_courses': completed_courses,
        'all_courses': all_courses,
        'recommended_courses': recommended_courses,
        'enrolled_count': enrolled_courses.count(),
        'completed_count': completed_courses.count(),
    }
    
    return render(request, 'courses/user_dashboard.html', context)

# Course List View
def course_list(request):
    courses = Course.objects.filter(is_active=True).annotate(
        enrollment_count=Count('enrollments')
    )
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        courses = courses.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    # Filter by type
    course_type = request.GET.get('type', '')
    if course_type:
        courses = courses.filter(course_type=course_type)
    
    context = {
        'courses': courses,
        'search_query': search_query,
        'course_type': course_type,
    }
    
    return render(request, 'courses/course_list.html', context)

# Course Detail View
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id, is_active=True)
    modules = course.modules.all()
    
    is_enrolled = False
    enrollment = None
    
    if request.user.is_authenticated:
        try:
            enrollment = Enrollment.objects.get(user=request.user, course=course, is_active=True)
            is_enrolled = True
        except Enrollment.DoesNotExist:
            pass
    
    context = {
        'course': course,
        'modules': modules,
        'is_enrolled': is_enrolled,
        'enrollment': enrollment,
    }
    
    return render(request, 'courses/course_detail.html', context)

# Course View (Learning Page)
@login_required
def course_view(request, course_id):
    course = get_object_or_404(Course, id=course_id, is_active=True)
    
    # Check if user is enrolled
    try:
        enrollment = Enrollment.objects.get(user=request.user, course=course, is_active=True)
    except Enrollment.DoesNotExist:
        messages.error(request, 'You need to enroll in this course first.')
        return redirect('course_detail', course_id=course.id)
    
    modules = course.modules.all()
    
    # Get module progress and attach to modules
    completed_module_ids = list(
        ModuleProgress.objects.filter(
            enrollment=enrollment,
            is_completed=True
        ).values_list('module_id', flat=True)
    )
    
    # Add completed status to each module
    for module in modules:
        module.is_completed = module.id in completed_module_ids
    
    # Get current module from URL parameter or default to first incomplete
    module_id_param = request.GET.get('module')
    current_module = None
    
    if module_id_param:
        # Try to get the module specified in URL
        try:
            current_module = modules.filter(id=int(module_id_param)).first()
        except (ValueError, TypeError):
            pass
    
    # If no module specified or not found, get first incomplete module
    if not current_module:
        for module in modules:
            if module.id not in completed_module_ids:
                current_module = module
                break
    
    # If all modules complete, show first module
    if not current_module and modules:
        current_module = modules.first()
    
    # Check if all modules are completed
    total_modules = modules.count()
    completed_count = len(completed_module_ids)
    all_modules_completed = (total_modules > 0 and completed_count == total_modules)
    
    context = {
        'course': course,
        'modules': modules,
        'enrollment': enrollment,
        'current_module': current_module,
        'completed_module_ids': completed_module_ids,
        'all_modules_completed': all_modules_completed,
    }
    
    return render(request, 'courses/course_view.html', context)

# Mark Module Complete
@login_required
def mark_module_complete(request, module_id):
    if request.method == 'POST':
        module = get_object_or_404(Module, id=module_id)
        
        try:
            enrollment = Enrollment.objects.get(
                user=request.user, 
                course=module.course, 
                is_active=True
            )
        except Enrollment.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Not enrolled'})
        
        # Create or update module progress
        progress, created = ModuleProgress.objects.get_or_create(
            enrollment=enrollment,
            module=module
        )
        progress.is_completed = True
        progress.completed_at = timezone.now()
        progress.save()
        
        # Update overall course progress
        total_modules = module.course.modules.count()
        completed_modules = ModuleProgress.objects.filter(
            enrollment=enrollment,
            is_completed=True
        ).count()
        
        if total_modules > 0:
            enrollment.progress = int((completed_modules / total_modules) * 100)
            if enrollment.progress == 100:
                enrollment.completed_at = timezone.now()
            enrollment.save()
        
        return JsonResponse({
            'success': True, 
            'progress': enrollment.progress,
            'message': 'Module marked as complete'
        })
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})

# Finish Course
@login_required
def finish_course(request, course_id):
    """Mark course as finished and show completion certificate/message"""
    course = get_object_or_404(Course, id=course_id, is_active=True)
    
    try:
        enrollment = Enrollment.objects.get(
            user=request.user,
            course=course,
            is_active=True
        )
    except Enrollment.DoesNotExist:
        messages.error(request, 'You are not enrolled in this course.')
        return redirect('course_detail', course_id=course.id)
    
    # Verify all modules are completed
    total_modules = course.modules.count()
    completed_modules = ModuleProgress.objects.filter(
        enrollment=enrollment,
        is_completed=True
    ).count()
    
    if completed_modules < total_modules:
        messages.warning(request, 'Please complete all modules before finishing the course.')
        return redirect('course_view', course_id=course.id)
    
    # Update enrollment
    if enrollment.progress != 100:
        enrollment.progress = 100
        enrollment.completed_at = timezone.now()
        enrollment.save()
    
    messages.success(request, f'🎉 Congratulations! You have completed {course.title}!')
    return render(request, 'courses/course_complete.html', {
        'course': course,
        'enrollment': enrollment,
    })
