from django import forms
from .models import Course, Module

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'short_description', 'image', 'video_url', 
                  'video_file', 'course_type', 'price', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Course Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Detailed Description'}),
            'short_description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Short Description'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'video_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'YouTube URL (optional)'}),
            'video_file': forms.FileInput(attrs={'class': 'form-control'}),
            'course_type': forms.Select(attrs={'class': 'form-select'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00', 'step': '0.01'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['title', 'description', 'module_type', 'order', 'video_url', 
                  'video_file', 'text_content', 'pdf_file', 'duration_minutes', 'is_preview']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Module Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'module_type': forms.Select(attrs={'class': 'form-select'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'video_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Video URL'}),
            'video_file': forms.FileInput(attrs={'class': 'form-control'}),
            'text_content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'pdf_file': forms.FileInput(attrs={'class': 'form-control'}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_preview': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
