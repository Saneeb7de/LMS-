"""
Script to initialize the LMS platform with sample data
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms_platform.settings')
django.setup()

from accounts.models import User
from courses.models import Course, Module
from django.utils import timezone

def setup_admin():
    """Set up admin user"""
    try:
        admin = User.objects.get(username='admin')
        admin.set_password('admin123')  # Set password
        admin.user_type = 'admin'
        admin.is_staff = True
        admin.is_superuser = True
        admin.save()
        print("✓ Admin user configured successfully")
        print("  Username: admin")
        print("  Password: admin123")
    except User.DoesNotExist:
        print("✗ Admin user not found. Please create superuser first.")

def create_sample_student():
    """Create a sample student user"""
    try:
        student, created = User.objects.get_or_create(
            username='student',
            defaults={
                'email': 'student@lms.com',
                'user_type': 'student',
                'first_name': 'John',
                'last_name': 'Doe'
            }
        )
        if created:
            student.set_password('student123')
            student.save()
            print("✓ Sample student user created")
            print("  Username: student")
            print("  Password: student123")
        else:
            print("  Sample student already exists")
    except Exception as e:
        print(f"✗ Error creating student: {e}")

def create_sample_courses():
    """Create sample courses"""
    try:
        admin = User.objects.get(username='admin')
        
        # Free Course
        course1, created1 = Course.objects.get_or_create(
            title='Introduction to Python Programming',
            defaults={
                'short_description': 'Learn Python basics from scratch',
                'description': 'A comprehensive introduction to Python programming covering variables, data types, control structures, functions, and object-oriented programming.',
                'course_type': 'free',
                'price': 0,
                'created_by': admin,
                'is_active': True
            }
        )
        
        if created1:
            # Add modules to free course
            Module.objects.create(
                course=course1,
                title='Getting Started with Python',
                description='Introduction to Python and setting up your environment',
                module_type='text',
                order=1,
                text_content='<h3>Welcome to Python!</h3><p>Python is a powerful, easy-to-learn programming language...</p>',
                duration_minutes=15,
                is_preview=True
            )
            
            Module.objects.create(
                course=course1,
                title='Variables and Data Types',
                description='Understanding Python variables and data types',
                module_type='video',
                order=2,
                video_url='https://www.youtube.com/embed/rfscVS0vtbw',
                duration_minutes=20,
                is_preview=False
            )
            
            Module.objects.create(
                course=course1,
                title='Control Structures',
                description='Learn about if-else statements and loops',
                module_type='text',
                order=3,
                text_content='<h3>Control Structures</h3><p>Control structures allow you to control the flow of your program...</p>',
                duration_minutes=25,
                is_preview=False
            )
            
            print("✓ Free course 'Introduction to Python Programming' created with modules")
        
        # Paid Course
        course2, created2 = Course.objects.get_or_create(
            title='Advanced Web Development with Django',
            defaults={
                'short_description': 'Master Django framework for web development',
                'description': 'Learn to build production-ready web applications using Django. Covers models, views, templates, authentication, and deployment.',
                'course_type': 'paid',
                'price': 1999.00,
                'created_by': admin,
                'is_active': True
            }
        )
        
        if created2:
            # Add modules to paid course
            Module.objects.create(
                course=course2,
                title='Django Overview',
                description='Introduction to Django framework',
                module_type='video',
                order=1,
                video_url='https://www.youtube.com/embed/F5mRW0jo-U4',
                duration_minutes=30,
                is_preview=True
            )
            
            Module.objects.create(
                course=course2,
                title='Django Models and ORM',
                description='Working with Django models and database',
                module_type='text',
                order=2,
                text_content='<h3>Django Models</h3><p>Models are Python classes that represent database tables...</p>',
                duration_minutes=45,
                is_preview=False
            )
            
            Module.objects.create(
                course=course2,
                title='Django Views and URLs',
                description='Creating views and URL routing',
                module_type='text',
                order=3,
                text_content='<h3>Views and URLs</h3><p>Views handle the logic of your application...</p>',
                duration_minutes=40,
                is_preview=False
            )
            
            print("✓ Paid course 'Advanced Web Development with Django' created with modules")
        
        # Another free course
        course3, created3 = Course.objects.get_or_create(
            title='Data Science Fundamentals',
            defaults={
                'short_description': 'Introduction to Data Science and Analytics',
                'description': 'Learn the basics of data science including statistics, data visualization, and machine learning concepts.',
                'course_type': 'free',
                'price': 0,
                'created_by': admin,
                'is_active': True
            }
        )
        
        if created3:
            Module.objects.create(
                course=course3,
                title='What is Data Science?',
                description='Overview of Data Science field',
                module_type='text',
                order=1,
                text_content='<h3>Data Science</h3><p>Data Science is an interdisciplinary field...</p>',
                duration_minutes=20,
                is_preview=True
            )
            
            print("✓ Free course 'Data Science Fundamentals' created with modules")
        
        print(f"\n✓ Total courses: {Course.objects.count()}")
        print(f"✓ Total modules: {Module.objects.count()}")
        
    except Exception as e:
        print(f"✗ Error creating courses: {e}")

if __name__ == '__main__':
    print("=" * 60)
    print("LMS PLATFORM - INITIALIZATION SCRIPT")
    print("=" * 60)
    print("\n1. Setting up admin user...")
    setup_admin()
    
    print("\n2. Creating sample student...")
    create_sample_student()
    
    print("\n3. Creating sample courses...")
    create_sample_courses()
    
    print("\n" + "=" * 60)
    print("SETUP COMPLETE!")
    print("=" * 60)
    print("\nYou can now:")
    print("1. Start the server: python manage.py runserver")
    print("2. Admin login: http://127.0.0.1:8000/accounts/admin-login/")
    print("   Username: admin | Password: admin123")
    print("3. User login: http://127.0.0.1:8000/accounts/login/")
    print("   Username: student | Password: student123")
    print("\n" + "=" * 60)
