from django.urls import path
from . import views, admin_views

urlpatterns = [
    # User-facing URLs
    path('', views.user_dashboard, name='user_dashboard'),
    path('browse/', views.course_list, name='course_list'),
    path('<int:course_id>/', views.course_detail, name='course_detail'),
    path('<int:course_id>/learn/', views.course_view, name='course_view'),
    path('module/<int:module_id>/complete/', views.mark_module_complete, name='mark_module_complete'),
    path('<int:course_id>/finish/', views.finish_course, name='finish_course'),
    
    # Admin URLs
    path('admin/courses/', admin_views.admin_course_list, name='admin_course_list'),
    path('admin/courses/create/', admin_views.admin_course_create, name='admin_course_create'),
    path('admin/courses/<int:course_id>/edit/', admin_views.admin_course_edit, name='admin_course_edit'),
    path('admin/courses/<int:course_id>/delete/', admin_views.admin_course_delete, name='admin_course_delete'),
    path('admin/courses/<int:course_id>/module/create/', admin_views.admin_module_create, name='admin_module_create'),
    path('admin/module/<int:module_id>/edit/', admin_views.admin_module_edit, name='admin_module_edit'),
    path('admin/module/<int:module_id>/delete/', admin_views.admin_module_delete, name='admin_module_delete'),
    path('admin/analytics/', admin_views.admin_analytics, name='admin_analytics'),
    path('admin/export-csv/', admin_views.export_data_csv, name='export_data_csv'),
]
