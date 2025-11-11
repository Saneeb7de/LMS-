from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('admin', 'Admin'),
        ('student', 'Student'),
    )
    
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='student')
    phone = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.username} ({self.user_type})"
    
    @property
    def is_admin_user(self):
        return self.user_type == 'admin'
    
    @property
    def is_student_user(self):
        return self.user_type == 'student'
