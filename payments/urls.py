from django.urls import path
from . import views

urlpatterns = [
    path('enroll/<int:course_id>/', views.enroll_course, name='enroll_course'),
    path('create-order/<int:course_id>/', views.create_order, name='create_order'),
    path('verify-payment/', views.verify_payment, name='verify_payment'),
    path('demo-enroll/<int:course_id>/', views.demo_enroll, name='demo_enroll'),
    path('success/<int:course_id>/', views.payment_success, name='payment_success'),
    path('failed/', views.payment_failed, name='payment_failed'),
]
