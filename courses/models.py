from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator

class Course(models.Model):
    COURSE_TYPE_CHOICES = (
        ('free', 'Free'),
        ('paid', 'Paid'),
    )
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    short_description = models.CharField(max_length=500, blank=True)
    image = models.ImageField(upload_to='course_images/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True, help_text="YouTube URL or other video link")
    video_file = models.FileField(upload_to='course_videos/', blank=True, null=True)
    course_type = models.CharField(max_length=10, choices=COURSE_TYPE_CHOICES, default='free')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, validators=[MinValueValidator(0)])
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_courses')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    @property
    def is_free(self):
        return self.course_type == 'free' or self.price == 0
    
    @property
    def enrolled_count(self):
        return self.enrollments.filter(is_active=True).count()


class Module(models.Model):
    MODULE_TYPE_CHOICES = (
        ('video', 'Video'),
        ('text', 'Text/Article'),
        ('pdf', 'PDF Document'),
        ('quiz', 'Quiz'),
    )
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    module_type = models.CharField(max_length=10, choices=MODULE_TYPE_CHOICES, default='text')
    order = models.PositiveIntegerField(default=0)
    
    # Content fields
    video_url = models.URLField(blank=True, null=True)
    video_file = models.FileField(upload_to='module_videos/', blank=True, null=True)
    text_content = models.TextField(blank=True)
    pdf_file = models.FileField(upload_to='module_pdfs/', blank=True, null=True)
    
    duration_minutes = models.PositiveIntegerField(default=0, help_text="Estimated duration in minutes")
    is_preview = models.BooleanField(default=False, help_text="Can be viewed without enrollment")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Enrollment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    progress = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)], help_text="Percentage of completion")
    completed_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        unique_together = ('user', 'course')
        ordering = ['-enrolled_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.course.title}"


class ModuleProgress(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='module_progress')
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        unique_together = ('enrollment', 'module')
    
    def __str__(self):
        return f"{self.enrollment.user.username} - {self.module.title}"
