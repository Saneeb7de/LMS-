from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from courses.models import Course, Enrollment
from .models import Payment
import razorpay
import json

# Initialize Razorpay client
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id, is_active=True)
    
    # Check if already enrolled
    existing_enrollment = Enrollment.objects.filter(
        user=request.user,
        course=course,
        is_active=True
    ).first()
    
    if existing_enrollment:
        messages.info(request, 'You are already enrolled in this course!')
        return redirect('course_view', course_id=course.id)
    
    # If free course, enroll directly (handle both GET and POST)
    if course.is_free:
        if request.method == 'POST' or request.method == 'GET':
            enrollment = Enrollment.objects.create(
                user=request.user,
                course=course
            )
            messages.success(request, 'Successfully enrolled in the course!')
            return redirect('course_view', course_id=course.id)
    
    # If paid course, show payment page
    context = {
        'course': course,
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
    }
    
    return render(request, 'payments/enroll_course.html', context)

@login_required
def create_order(request, course_id):
    if request.method == 'POST':
        course = get_object_or_404(Course, id=course_id, is_active=True)
        
        # Check if already enrolled
        existing_enrollment = Enrollment.objects.filter(
            user=request.user,
            course=course,
            is_active=True
        ).first()
        
        if existing_enrollment:
            return JsonResponse({'success': False, 'message': 'Already enrolled'})
        
        # Create Razorpay order
        amount = int(course.price * 100)  # Convert to paise
        
        # Use real Razorpay integration
        try:
            razorpay_order = razorpay_client.order.create({
                'amount': amount,
                'currency': 'INR',
                'payment_capture': 1
            })
            
            # Create payment record
            payment = Payment.objects.create(
                user=request.user,
                course=course,
                amount=course.price,
                razorpay_order_id=razorpay_order['id'],
                payment_status='pending'
            )
            
            return JsonResponse({
                'success': True,
                'order_id': razorpay_order['id'],
                'amount': amount,
                'currency': 'INR',
                'key_id': settings.RAZORPAY_KEY_ID,
            })
        
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})

@csrf_exempt
@login_required
def verify_payment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            razorpay_payment_id = data.get('razorpay_payment_id')
            razorpay_order_id = data.get('razorpay_order_id')
            razorpay_signature = data.get('razorpay_signature')
            
            # Verify signature
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            }
            
            try:
                razorpay_client.utility.verify_payment_signature(params_dict)
                
                # Update payment record
                payment = Payment.objects.get(razorpay_order_id=razorpay_order_id)
                payment.razorpay_payment_id = razorpay_payment_id
                payment.razorpay_signature = razorpay_signature
                payment.payment_status = 'completed'
                payment.save()
                
                # Create enrollment
                enrollment = Enrollment.objects.create(
                    user=request.user,
                    course=payment.course
                )
                
                return JsonResponse({
                    'success': True,
                    'message': 'Payment successful! You are now enrolled.',
                    'course_id': payment.course.id
                })
            
            except razorpay.errors.SignatureVerificationError:
                # Update payment as failed
                payment = Payment.objects.get(razorpay_order_id=razorpay_order_id)
                payment.payment_status = 'failed'
                payment.save()
                
                return JsonResponse({'success': False, 'message': 'Payment verification failed'})
        
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})

@login_required
def payment_success(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    context = {
        'course': course
    }
    
    return render(request, 'payments/payment_success.html', context)

@login_required
def payment_failed(request):
    return render(request, 'payments/payment_failed.html')

@login_required
def demo_enroll(request, course_id):
    """Demo endpoint to simulate payment enrollment for testing"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            order_id = data.get('order_id')
            
            # Get the payment record
            payment = Payment.objects.filter(razorpay_order_id=order_id).first()
            
            if not payment:
                return JsonResponse({'success': False, 'message': 'Payment record not found'})
            
            # Check if already enrolled
            existing_enrollment = Enrollment.objects.filter(
                user=request.user,
                course=payment.course,
                is_active=True
            ).first()
            
            if existing_enrollment:
                return JsonResponse({'success': False, 'message': 'Already enrolled'})
            
            # Update payment as completed (demo)
            payment.payment_status = 'completed'
            payment.razorpay_payment_id = f"pay_demo_{order_id[-10:]}"
            payment.razorpay_signature = f"sig_demo_{order_id[-10:]}"
            payment.notes = 'Demo Mode - Simulated Payment'
            payment.save()
            
            # Create enrollment
            enrollment = Enrollment.objects.create(
                user=request.user,
                course=payment.course
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Demo enrollment successful!',
                'course_id': payment.course.id
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})
