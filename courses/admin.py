from django.contrib import admin
from .models import Course, Module, Enrollment, ModuleProgress

class ModuleInline(admin.TabularInline):
    model = Module
    extra = 1

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'course_type', 'price', 'created_by', 'is_active', 'created_at')
    list_filter = ('course_type', 'is_active', 'created_at')
    search_fields = ('title', 'description')
    inlines = [ModuleInline]

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'module_type', 'order', 'is_preview')
    list_filter = ('module_type', 'is_preview')
    search_fields = ('title', 'course__title')

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'enrolled_at', 'is_active', 'progress')
    list_filter = ('is_active', 'enrolled_at')
    search_fields = ('user__username', 'course__title')

@admin.register(ModuleProgress)
class ModuleProgressAdmin(admin.ModelAdmin):
    list_display = ('enrollment', 'module', 'is_completed', 'completed_at')
    list_filter = ('is_completed',)
