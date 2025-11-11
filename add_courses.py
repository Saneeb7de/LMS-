"""
Script to add 10 diverse courses to the LMS platform
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms_platform.settings')
django.setup()

from accounts.models import User
from courses.models import Course, Module

def add_courses():
    """Add 10 courses with modules"""
    
    # Get admin user
    try:
        admin = User.objects.get(username='admin')
    except User.DoesNotExist:
        print("❌ Admin user not found. Please create an admin user first.")
        return
    
    courses_data = [
        {
            'title': 'Complete Python Bootcamp 2025',
            'short_description': 'Master Python from beginner to advanced level',
            'description': 'Learn Python programming from scratch. This comprehensive course covers everything from basic syntax to advanced topics like decorators, generators, and async programming. Perfect for beginners and intermediate developers.',
            'course_type': 'free',
            'price': 0,
            'modules': [
                {'title': 'Python Basics & Setup', 'type': 'video', 'url': 'https://www.youtube.com/embed/rfscVS0vtbw', 'duration': 25, 'order': 1, 'preview': True},
                {'title': 'Variables & Data Types', 'type': 'video', 'url': 'https://www.youtube.com/embed/LKYFc6WsMAA', 'duration': 20, 'order': 2},
                {'title': 'Control Flow - If/Else', 'type': 'video', 'url': 'https://www.youtube.com/embed/PqFKRqpHrjw', 'duration': 18, 'order': 3},
                {'title': 'Loops & Iterations', 'type': 'video', 'url': 'https://www.youtube.com/embed/94UHCEmprCY', 'duration': 22, 'order': 4},
                {'title': 'Functions & Modules', 'type': 'video', 'url': 'https://www.youtube.com/embed/9Os0o3wzS_I', 'duration': 30, 'order': 5},
                {'title': 'Lists & Tuples', 'type': 'video', 'url': 'https://www.youtube.com/embed/tw7ror9x32s', 'duration': 25, 'order': 6},
                {'title': 'Dictionaries & Sets', 'type': 'video', 'url': 'https://www.youtube.com/embed/XCcpzWs-CI4', 'duration': 20, 'order': 7},
                {'title': 'File Handling', 'type': 'video', 'url': 'https://www.youtube.com/embed/Uh2ebFW8OYM', 'duration': 28, 'order': 8},
            ]
        },
        {
            'title': 'Web Development Masterclass',
            'short_description': 'Full-stack web development with HTML, CSS, JavaScript, and React',
            'description': 'Become a professional web developer. Learn HTML5, CSS3, JavaScript ES6+, React, Node.js, and deploy real-world projects. Build responsive websites and modern web applications.',
            'course_type': 'paid',
            'price': 2499,
            'modules': [
                {'title': 'HTML5 Fundamentals', 'type': 'video', 'url': 'https://www.youtube.com/embed/pQN-pnXPaVg', 'duration': 35, 'order': 1, 'preview': True},
                {'title': 'CSS3 Basics', 'type': 'video', 'url': 'https://www.youtube.com/embed/OXGznpKZ_sA', 'duration': 30, 'order': 2},
                {'title': 'CSS Flexbox Tutorial', 'type': 'video', 'url': 'https://www.youtube.com/embed/JJSoEo8JSnc', 'duration': 25, 'order': 3},
                {'title': 'CSS Grid Layout', 'type': 'video', 'url': 'https://www.youtube.com/embed/EFafSYg-PkI', 'duration': 28, 'order': 4},
                {'title': 'JavaScript Essentials', 'type': 'video', 'url': 'https://www.youtube.com/embed/W6NZfCO5SIk', 'duration': 45, 'order': 5},
                {'title': 'DOM Manipulation', 'type': 'video', 'url': 'https://www.youtube.com/embed/wiozYyXQEVk', 'duration': 32, 'order': 6},
                {'title': 'Async JavaScript & Fetch API', 'type': 'video', 'url': 'https://www.youtube.com/embed/cuEtnrL9-H0', 'duration': 38, 'order': 7},
                {'title': 'React Fundamentals', 'type': 'video', 'url': 'https://www.youtube.com/embed/SqcY0GlETPk', 'duration': 50, 'order': 8},
                {'title': 'Building React Projects', 'type': 'video', 'url': 'https://www.youtube.com/embed/Ke90Tje7VS0', 'duration': 55, 'order': 9},
            ]
        },
        {
            'title': 'Machine Learning with Python',
            'short_description': 'Learn ML algorithms, scikit-learn, and TensorFlow',
            'description': 'Comprehensive machine learning course covering supervised and unsupervised learning, neural networks, deep learning, and real-world ML projects using Python, NumPy, Pandas, and TensorFlow.',
            'course_type': 'paid',
            'price': 3999,
            'modules': [
                {'title': 'Introduction to ML', 'type': 'video', 'url': 'https://www.youtube.com/embed/7eh4d6sabA0', 'duration': 40, 'order': 1, 'preview': True},
                {'title': 'NumPy Fundamentals', 'type': 'video', 'url': 'https://www.youtube.com/embed/QUT1VHiLmmI', 'duration': 35, 'order': 2},
                {'title': 'Pandas for Data Analysis', 'type': 'video', 'url': 'https://www.youtube.com/embed/vmEHCJofslg', 'duration': 42, 'order': 3},
                {'title': 'Data Visualization with Matplotlib', 'type': 'video', 'url': 'https://www.youtube.com/embed/DAQNHzOcO5A', 'duration': 30, 'order': 4},
                {'title': 'Linear Regression', 'type': 'video', 'url': 'https://www.youtube.com/embed/7ArmBVF2dCs', 'duration': 35, 'order': 5},
                {'title': 'Logistic Regression', 'type': 'video', 'url': 'https://www.youtube.com/embed/yIYKR4sgzI8', 'duration': 32, 'order': 6},
                {'title': 'Decision Trees', 'type': 'video', 'url': 'https://www.youtube.com/embed/ZVR2Way4nwQ', 'duration': 28, 'order': 7},
                {'title': 'Neural Networks Basics', 'type': 'video', 'url': 'https://www.youtube.com/embed/aircAruvnKk', 'duration': 45, 'order': 8},
                {'title': 'TensorFlow Tutorial', 'type': 'video', 'url': 'https://www.youtube.com/embed/tPYj3fFJGjk', 'duration': 50, 'order': 9},
            ]
        },
        {
            'title': 'Digital Marketing Strategy',
            'short_description': 'SEO, Social Media, Content Marketing & Analytics',
            'description': 'Master digital marketing strategies. Learn SEO optimization, social media marketing, content marketing, email campaigns, Google Analytics, and Facebook Ads to grow your business online.',
            'course_type': 'free',
            'price': 0,
            'modules': [
                {'title': 'Digital Marketing Overview', 'type': 'video', 'url': 'https://www.youtube.com/embed/bixR-KIJKYM', 'duration': 25, 'order': 1, 'preview': True},
                {'title': 'SEO Fundamentals', 'type': 'video', 'url': 'https://www.youtube.com/embed/DvwS7cV9GmQ', 'duration': 30, 'order': 2},
                {'title': 'Keyword Research', 'type': 'video', 'url': 'https://www.youtube.com/embed/hOnlLRrV1vw', 'duration': 22, 'order': 3},
                {'title': 'Content Marketing Strategy', 'type': 'video', 'url': 'https://www.youtube.com/embed/xKjBlXaBVH0', 'duration': 28, 'order': 4},
                {'title': 'Social Media Marketing', 'type': 'video', 'url': 'https://www.youtube.com/embed/BQ8KzOOWv-c', 'duration': 35, 'order': 5},
                {'title': 'Facebook Ads Tutorial', 'type': 'video', 'url': 'https://www.youtube.com/embed/lGfcxHZ-fA8', 'duration': 40, 'order': 6},
                {'title': 'Google Analytics', 'type': 'video', 'url': 'https://www.youtube.com/embed/gBeMELnxdIg', 'duration': 32, 'order': 7},
                {'title': 'Email Marketing Basics', 'type': 'video', 'url': 'https://www.youtube.com/embed/IYiNc7iS0lA', 'duration': 26, 'order': 8},
            ]
        },
        {
            'title': 'Mobile App Development with React Native',
            'short_description': 'Build iOS and Android apps with JavaScript',
            'description': 'Create cross-platform mobile applications using React Native. Build real apps for both iOS and Android with a single codebase. Learn navigation, state management, and API integration.',
            'course_type': 'paid',
            'price': 2999,
            'modules': [
                {'title': 'React Native Setup', 'type': 'video', 'url': 'https://www.youtube.com/embed/0-S5a0eXPoc', 'duration': 30, 'order': 1, 'preview': True},
                {'title': 'Core Components', 'type': 'video', 'url': 'https://www.youtube.com/embed/ur6I5m2nTvk', 'duration': 35, 'order': 2},
                {'title': 'Styling in React Native', 'type': 'video', 'url': 'https://www.youtube.com/embed/Fpl7xyNTMqk', 'duration': 28, 'order': 3},
                {'title': 'State Management with Hooks', 'type': 'video', 'url': 'https://www.youtube.com/embed/O6P86uwfdR0', 'duration': 32, 'order': 4},
                {'title': 'Navigation in React Native', 'type': 'video', 'url': 'https://www.youtube.com/embed/nQVCkqvU1uE', 'duration': 35, 'order': 5},
                {'title': 'API Integration & Fetch', 'type': 'video', 'url': 'https://www.youtube.com/embed/VqYz8galZXg', 'duration': 30, 'order': 6},
                {'title': 'AsyncStorage & Data Persistence', 'type': 'video', 'url': 'https://www.youtube.com/embed/Me2nJdDa8S8', 'duration': 25, 'order': 7},
                {'title': 'Building a Todo App', 'type': 'video', 'url': 'https://www.youtube.com/embed/0kL6nhutjQ8', 'duration': 45, 'order': 8},
            ]
        },
        {
            'title': 'Graphic Design with Adobe Creative Suite',
            'short_description': 'Master Photoshop, Illustrator, and InDesign',
            'description': 'Professional graphic design course covering Adobe Photoshop, Illustrator, and InDesign. Learn logo design, photo editing, typography, and create stunning visual content for print and digital media.',
            'course_type': 'paid',
            'price': 1999,
            'modules': [
                {'title': 'Design Principles', 'type': 'video', 'url': 'https://www.youtube.com/embed/YqQx75OPRa0', 'duration': 28, 'order': 1, 'preview': True},
                {'title': 'Color Theory for Designers', 'type': 'video', 'url': 'https://www.youtube.com/embed/_2LLXnUdUIc', 'duration': 22, 'order': 2},
                {'title': 'Typography Essentials', 'type': 'video', 'url': 'https://www.youtube.com/embed/sByzHoiYFX0', 'duration': 20, 'order': 3},
                {'title': 'Photoshop Basics', 'type': 'video', 'url': 'https://www.youtube.com/embed/IyR_uYsRdPs', 'duration': 40, 'order': 4},
                {'title': 'Photo Editing Techniques', 'type': 'video', 'url': 'https://www.youtube.com/embed/bKFALLbZcto', 'duration': 35, 'order': 5},
                {'title': 'Illustrator for Logos', 'type': 'video', 'url': 'https://www.youtube.com/embed/Ib8UBwu3yGA', 'duration': 35, 'order': 6},
                {'title': 'Creating Vector Graphics', 'type': 'video', 'url': 'https://www.youtube.com/embed/z99EQGV8axw', 'duration': 30, 'order': 7},
                {'title': 'InDesign Layout Design', 'type': 'video', 'url': 'https://www.youtube.com/embed/B5bN2YKnfaI', 'duration': 38, 'order': 8},
            ]
        },
        {
            'title': 'Financial Literacy & Investment',
            'short_description': 'Personal finance, stocks, and wealth building',
            'description': 'Learn personal finance management, budgeting, investing in stocks and mutual funds, retirement planning, and building wealth. Understand financial markets and make informed investment decisions.',
            'course_type': 'free',
            'price': 0,
            'modules': [
                {'title': 'Personal Finance 101', 'type': 'video', 'url': 'https://www.youtube.com/embed/Rnn7ans_ugo', 'duration': 25, 'order': 1, 'preview': True},
                {'title': 'Budgeting & Saving Money', 'type': 'video', 'url': 'https://www.youtube.com/embed/HQzoZfc3GwQ', 'duration': 20, 'order': 2},
                {'title': 'Understanding Credit Scores', 'type': 'video', 'url': 'https://www.youtube.com/embed/LFVGR6QDcbk', 'duration': 18, 'order': 3},
                {'title': 'Introduction to Investing', 'type': 'video', 'url': 'https://www.youtube.com/embed/gFQNPmLKj1k', 'duration': 30, 'order': 4},
                {'title': 'Stock Market Basics', 'type': 'video', 'url': 'https://www.youtube.com/embed/p7HKvqRI_Bo', 'duration': 25, 'order': 5},
                {'title': 'Mutual Funds & ETFs', 'type': 'video', 'url': 'https://www.youtube.com/embed/OwRh1F7M6Ic', 'duration': 22, 'order': 6},
                {'title': 'Retirement Planning', 'type': 'video', 'url': 'https://www.youtube.com/embed/gvZSpET11ZY', 'duration': 28, 'order': 7},
                {'title': 'Real Estate Investing', 'type': 'video', 'url': 'https://www.youtube.com/embed/Eb_BXhNF7bU', 'duration': 32, 'order': 8},
            ]
        },
        {
            'title': 'Ethical Hacking & Cybersecurity',
            'short_description': 'Learn penetration testing and network security',
            'description': 'Become a certified ethical hacker. Learn penetration testing, network security, vulnerability assessment, cryptography, and secure coding practices. Protect systems from cyber threats.',
            'course_type': 'paid',
            'price': 4999,
            'modules': [
                {'title': 'Introduction to Cybersecurity', 'type': 'video', 'url': 'https://www.youtube.com/embed/inWWhr5tnEA', 'duration': 35, 'order': 1, 'preview': True},
                {'title': 'Network Security Basics', 'type': 'video', 'url': 'https://www.youtube.com/embed/qM1YZGallQw', 'duration': 32, 'order': 2},
                {'title': 'Linux for Ethical Hacking', 'type': 'video', 'url': 'https://www.youtube.com/embed/U1w4T03B30I', 'duration': 38, 'order': 3},
                {'title': 'Kali Linux Tools', 'type': 'video', 'url': 'https://www.youtube.com/embed/lZAoFs75_cs', 'duration': 40, 'order': 4},
                {'title': 'Penetration Testing Basics', 'type': 'video', 'url': 'https://www.youtube.com/embed/3Kq1MIfTWCE', 'duration': 45, 'order': 5},
                {'title': 'Web Application Security', 'type': 'video', 'url': 'https://www.youtube.com/embed/WtHnT73NaaQ', 'duration': 35, 'order': 6},
                {'title': 'Cryptography Fundamentals', 'type': 'video', 'url': 'https://www.youtube.com/embed/jhXCTbFnK8o', 'duration': 30, 'order': 7},
                {'title': 'Ethical Hacking Projects', 'type': 'video', 'url': 'https://www.youtube.com/embed/fNzpcB7ODxQ', 'duration': 50, 'order': 8},
            ]
        },
        {
            'title': 'Content Writing & Copywriting',
            'short_description': 'Write compelling content that converts',
            'description': 'Master the art of writing. Learn SEO content writing, copywriting techniques, storytelling, email marketing copy, and create engaging content for blogs, websites, and social media.',
            'course_type': 'free',
            'price': 0,
            'modules': [
                {'title': 'Writing Fundamentals', 'type': 'video', 'url': 'https://www.youtube.com/embed/L-bFtFf3xl8', 'duration': 22, 'order': 1, 'preview': True},
                {'title': 'Grammar & Punctuation', 'type': 'video', 'url': 'https://www.youtube.com/embed/7gFQ1MqYDek', 'duration': 18, 'order': 2},
                {'title': 'Storytelling Techniques', 'type': 'video', 'url': 'https://www.youtube.com/embed/1nYFpuc2Umk', 'duration': 25, 'order': 3},
                {'title': 'SEO Content Writing', 'type': 'video', 'url': 'https://www.youtube.com/embed/3oec_c2hMAY', 'duration': 28, 'order': 4},
                {'title': 'Copywriting Techniques', 'type': 'video', 'url': 'https://www.youtube.com/embed/pWZ4PxRMcds', 'duration': 30, 'order': 5},
                {'title': 'Writing for Social Media', 'type': 'video', 'url': 'https://www.youtube.com/embed/V8_wc6WqqxE', 'duration': 20, 'order': 6},
                {'title': 'Email Copywriting', 'type': 'video', 'url': 'https://www.youtube.com/embed/bTPbTeYRgbg', 'duration': 24, 'order': 7},
                {'title': 'Blog Writing Strategies', 'type': 'video', 'url': 'https://www.youtube.com/embed/cOCVzd3lf_M', 'duration': 26, 'order': 8},
            ]
        },
        {
            'title': 'Cloud Computing with AWS',
            'short_description': 'Amazon Web Services certification preparation',
            'description': 'Complete AWS cloud computing course. Learn EC2, S3, Lambda, RDS, CloudFormation, and deploy scalable applications on Amazon Web Services. Prepare for AWS Solutions Architect certification.',
            'course_type': 'paid',
            'price': 3499,
            'modules': [
                {'title': 'AWS Cloud Overview', 'type': 'video', 'url': 'https://www.youtube.com/embed/ulprqHHWlng', 'duration': 40, 'order': 1, 'preview': True},
                {'title': 'AWS Account Setup', 'type': 'video', 'url': 'https://www.youtube.com/embed/xi-JDeceLeI', 'duration': 25, 'order': 2},
                {'title': 'EC2 Instance Tutorial', 'type': 'video', 'url': 'https://www.youtube.com/embed/iHX-jtKIVNA', 'duration': 35, 'order': 3},
                {'title': 'S3 Storage Services', 'type': 'video', 'url': 'https://www.youtube.com/embed/77lMCiiMilo', 'duration': 35, 'order': 4},
                {'title': 'AWS Lambda Functions', 'type': 'video', 'url': 'https://www.youtube.com/embed/eOBq__h4OJ4', 'duration': 32, 'order': 5},
                {'title': 'RDS Database Setup', 'type': 'video', 'url': 'https://www.youtube.com/embed/FzxqIdIZ9wc', 'duration': 30, 'order': 6},
                {'title': 'CloudFormation Templates', 'type': 'video', 'url': 'https://www.youtube.com/embed/t97jZch4lMY', 'duration': 38, 'order': 7},
                {'title': 'AWS Deployment Project', 'type': 'video', 'url': 'https://www.youtube.com/embed/7m_q1ldzw0U', 'duration': 45, 'order': 8},
            ]
        },
    ]
    
    print("=" * 60)
    print("ADDING 10 COURSES TO DATABASE")
    print("=" * 60)
    
    created_count = 0
    skipped_count = 0
    
    for course_data in courses_data:
        # Check if course already exists
        existing = Course.objects.filter(title=course_data['title']).first()
        
        if existing:
            print(f"\n⚠️  Course '{course_data['title']}' already exists - Skipping")
            skipped_count += 1
            continue
        
        # Create course
        modules_data = course_data.pop('modules')
        course = Course.objects.create(
            created_by=admin,
            is_active=True,
            **course_data
        )
        
        print(f"\n✅ Created: {course.title}")
        print(f"   Type: {course.get_course_type_display()}")
        print(f"   Price: ₹{course.price}")
        
        # Create modules
        for module_data in modules_data:
            module_type = module_data.pop('type')
            video_url = module_data.pop('url', None)
            text_content = module_data.pop('content', None)
            duration = module_data.pop('duration')
            order = module_data.pop('order')
            preview = module_data.pop('preview', False)
            
            module = Module.objects.create(
                course=course,
                title=module_data['title'],
                module_type=module_type,
                video_url=video_url if video_url else '',
                text_content=text_content if text_content else '',
                duration_minutes=duration,
                order=order,
                is_preview=preview
            )
            
            print(f"   📝 Module {order}: {module.title} ({module_type})")
        
        created_count += 1
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"✅ Courses Created: {created_count}")
    print(f"⚠️  Courses Skipped: {skipped_count}")
    print(f"📚 Total Courses in DB: {Course.objects.count()}")
    print(f"📝 Total Modules in DB: {Module.objects.count()}")
    print("=" * 60)

if __name__ == '__main__':
    add_courses()
