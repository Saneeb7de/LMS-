# LMS Platform - Learning Management System

A comprehensive Learning Management System built with Django that provides a seamless online learning experience with dual authentication (admin and user), course management, and integrated payment processing.

## Features

### 🎓 For Students
- **User Authentication**: Secure login and registration system
- **Course Browsing**: Search and filter courses by type (free/paid)
- **Course Enrollment**: Easy enrollment for free courses
- **Secure Payments**: Razorpay integration for premium courses
- **Learning Interface**: Interactive course player with video, text, and PDF modules
- **Progress Tracking**: Track completion status and overall course progress
- **Personalized Dashboard**: View enrolled courses and recommendations

### 👨‍💼 For Administrators
- **Admin Authentication**: Separate admin login portal
- **Course Management**: Create, edit, and delete courses
- **Module Management**: Add and organize course modules (video, text, PDF, quiz)
- **Analytics Dashboard**: View statistics on enrollments, revenue, and user engagement
- **User Management**: Monitor and manage registered users
- **Data Export**: Export platform data to CSV for analysis

### 💰 Payment Integration
- Razorpay payment gateway integration
- Support for both free and paid courses
- Secure payment verification
- Transaction tracking and history

## Technology Stack

- **Backend**: Django 5.x
- **Frontend**: Bootstrap 5, JavaScript
- **Database**: SQLite (default, can be changed to PostgreSQL/MySQL)
- **Payment**: Razorpay
- **Icons**: Font Awesome 6

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone or Navigate to Project Directory
```bash
cd c:\codersapworkshop\djangoproject
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure Razorpay (Optional, for payments)
Edit `lms_platform/settings.py` and add your Razorpay credentials:
```python
RAZORPAY_KEY_ID = 'your_razorpay_key_id'
RAZORPAY_KEY_SECRET = 'your_razorpay_key_secret'
```

### Step 4: Run Migrations
The migrations are already created. Run:
```bash
python manage.py migrate
```

### Step 5: Create a Superuser (Admin)
```bash
python manage.py createsuperuser
```
Follow the prompts to create an admin account.

### Step 6: Create Initial Admin User for Platform
After creating superuser, you need to mark it as admin in the system:
```bash
python manage.py shell
```
Then in the Python shell:
```python
from accounts.models import User
user = User.objects.get(username='your_superuser_username')
user.user_type = 'admin'
user.save()
exit()
```

### Step 7: Run the Development Server
```bash
python manage.py runserver
```

The application will be available at: `http://127.0.0.1:8000/`

## Usage Guide

### For Students

1. **Register**: Go to `/accounts/register/` to create a new account
2. **Login**: Access `/accounts/login/` to log in
3. **Browse Courses**: View all available courses at `/courses/browse/`
4. **Enroll**: 
   - For free courses: Click "Enroll Now" to start immediately
   - For paid courses: Click "Buy Now" and complete payment via Razorpay
5. **Learn**: Access enrolled courses from your dashboard and track progress

### For Administrators

1. **Login**: Access admin portal at `/accounts/admin-login/`
2. **Dashboard**: View platform statistics and quick actions
3. **Manage Courses**: 
   - Create new courses with title, description, images, and videos
   - Add modules (video, text, PDF, quiz)
   - Set pricing (free or paid)
   - Activate/deactivate courses
4. **Analytics**: View detailed reports on enrollments, revenue, and users
5. **Export Data**: Download platform data as CSV for external analysis

## Project Structure

```
djangoproject/
├── accounts/              # User authentication and profiles
│   ├── models.py         # User model with admin/student types
│   ├── views.py          # Login, register, logout views
│   └── forms.py          # Authentication forms
├── courses/              # Course and module management
│   ├── models.py         # Course, Module, Enrollment, ModuleProgress
│   ├── views.py          # User-facing course views
│   ├── admin_views.py    # Admin course management views
│   └── forms.py          # Course and module forms
├── payments/             # Payment processing
│   ├── models.py         # Payment transaction model
│   └── views.py          # Razorpay integration
├── templates/            # HTML templates
│   ├── base.html         # Base template with navigation
│   ├── accounts/         # Authentication templates
│   ├── courses/          # Course and learning templates
│   └── payments/         # Payment templates
├── static/               # Static files (CSS, JS, images)
├── media/                # User-uploaded files
└── lms_platform/         # Project settings and URLs
```

## Key Models

### User
- Custom user model with `user_type` (admin/student)
- Profile information (phone, bio, profile picture)

### Course
- Title, description, images, videos
- Course type (free/paid) and pricing
- Enrollment tracking

### Module
- Module types: video, text, PDF, quiz
- Ordered content within courses
- Duration and preview settings

### Enrollment
- User-course relationship
- Progress tracking (0-100%)
- Completion status

### Payment
- Razorpay integration
- Transaction tracking
- Payment status management

## Default Credentials

After setup, you can create test accounts:

**Admin Account:**
- Login at: `/accounts/admin-login/`
- Use the superuser credentials you created

**Student Account:**
- Register at: `/accounts/register/`
- Or use Django admin to create test users

## Features to Test

1. ✅ Admin login and dashboard
2. ✅ Create a new course with modules
3. ✅ Student registration and login
4. ✅ Browse and search courses
5. ✅ Enroll in a free course
6. ✅ Access course learning interface
7. ✅ Mark modules as complete
8. ✅ Track progress
9. ✅ Purchase a paid course (requires Razorpay setup)
10. ✅ View analytics and export data

## API Endpoints

### Authentication
- `GET/POST /accounts/login/` - User login
- `GET/POST /accounts/register/` - User registration
- `GET/POST /accounts/admin-login/` - Admin login
- `GET /accounts/logout/` - Logout

### Courses
- `GET /courses/` - User dashboard
- `GET /courses/browse/` - Course listing
- `GET /courses/<id>/` - Course details
- `GET /courses/<id>/learn/` - Course learning interface

### Admin
- `GET /accounts/admin-dashboard/` - Admin dashboard
- `GET /courses/admin/courses/` - Manage courses
- `GET/POST /courses/admin/courses/create/` - Create course
- `GET/POST /courses/admin/courses/<id>/edit/` - Edit course
- `GET /courses/admin/analytics/` - Analytics dashboard
- `GET /courses/admin/export-csv/` - Export data

### Payments
- `GET/POST /payments/enroll/<course_id>/` - Enroll/purchase
- `POST /payments/create-order/<course_id>/` - Create Razorpay order
- `POST /payments/verify-payment/` - Verify payment

## Notes

- **Static Files**: In production, run `python manage.py collectstatic`
- **Media Files**: Ensure proper permissions for media uploads
- **Database**: Default is SQLite. For production, use PostgreSQL or MySQL
- **Security**: Change `SECRET_KEY` in production and set `DEBUG = False`
- **Razorpay**: Add your credentials in settings for payment functionality

## Troubleshooting

### Issue: Static files not loading
**Solution**: Run `python manage.py collectstatic`

### Issue: Images not displaying
**Solution**: Check MEDIA_URL and MEDIA_ROOT settings, ensure directories exist

### Issue: Razorpay payments failing
**Solution**: Verify your Razorpay credentials in settings.py

### Issue: Admin can't access admin features
**Solution**: Ensure user.user_type is set to 'admin' in the database

## Future Enhancements

- 📱 Mobile responsive design improvements
- 🎥 Live class integration
- 💬 Discussion forums
- 📊 Advanced analytics and reporting
- 🎯 Quiz functionality with automated grading
- 🏆 Certificates upon course completion
- 📧 Email notifications
- 🔍 Advanced search and filtering
- 👥 Student profiles and achievements

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review Django documentation: https://docs.djangoproject.com/
3. Check Razorpay documentation: https://razorpay.com/docs/

## License

This project is created for educational purposes.

---

**Developed with Django** 🎓
#   L M S -  
 