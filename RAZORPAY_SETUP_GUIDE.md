# 💳 Razorpay Payment Integration - Complete Setup Guide

## 📋 Overview

This guide walks you through setting up Razorpay payment gateway integration for your LMS platform, enabling secure payment processing for premium courses.

---

## 🚀 Step 1: Create Razorpay Account

### 1.1 Sign Up
1. Visit [https://razorpay.com/](https://razorpay.com/)
2. Click **"Sign Up"** button
3. Fill in your details:
   - Email address
   - Mobile number
   - Password
4. Click **"Create Account"**
5. Verify your email and mobile number

### 1.2 Complete KYC (For Live Mode - Optional for Testing)
- For Test Mode: KYC not required
- For Live Mode: Complete business KYC verification

---

## 🔑 Step 2: Get API Keys

### 2.1 Login to Dashboard
1. Go to [https://dashboard.razorpay.com/](https://dashboard.razorpay.com/)
2. Login with your credentials

### 2.2 Switch to Test Mode
- At the top of the dashboard, you'll see a toggle
- Make sure **"Test Mode"** is enabled (it should show a colored indicator)
- Test Mode allows you to test payments without real money

### 2.3 Generate API Keys
1. Navigate to **Settings** (gear icon in left sidebar)
2. Click on **API Keys** (under "Website and app settings")
3. Click **"Generate Test Key"** or **"Generate Live Key"**
4. You'll see two keys generated:
   - **Key ID**: Starts with `rzp_test_` (for test mode)
   - **Key Secret**: Click "Show" to reveal

### 2.4 Copy Your Keys
```
Key ID:     rzp_test_XXXXXXXXXXXXX
Key Secret: XXXXXXXXXXXXXXXXXXXXXXXX
```

⚠️ **IMPORTANT**: 
- Never share your Key Secret publicly
- Never commit it to version control
- Keep it secure like a password

---

## ⚙️ Step 3: Configure Django Project

### 3.1 Update Settings File
Open `lms_platform/settings.py` and update:

```python
# Razorpay Configuration
RAZORPAY_KEY_ID = 'rzp_test_XXXXXXXXXXXXX'  # Replace with your Test Key ID
RAZORPAY_KEY_SECRET = 'XXXXXXXXXXXXXXXXXXXXXXXX'  # Replace with your Test Key Secret
```

### 3.2 For Production (Live Mode)
When going live:
1. Switch to **Live Mode** in Razorpay Dashboard
2. Generate **Live Keys** (starts with `rzp_live_`)
3. Update settings.py with live keys
4. Complete KYC verification

### 3.3 Using Environment Variables (Recommended)
Create a `.env` file:
```env
RAZORPAY_KEY_ID=rzp_test_XXXXXXXXXXXXX
RAZORPAY_KEY_SECRET=XXXXXXXXXXXXXXXXXXXXXXXX
```

Update `settings.py`:
```python
import os
from dotenv import load_dotenv

load_dotenv()

RAZORPAY_KEY_ID = os.getenv('RAZORPAY_KEY_ID', 'your_razorpay_key_id')
RAZORPAY_KEY_SECRET = os.getenv('RAZORPAY_KEY_SECRET', 'your_razorpay_key_secret')
```

Install python-dotenv:
```bash
pip install python-dotenv
```

---

## 🎯 Step 4: Test Payment Flow

### 4.1 Demo Mode (Current Setup)
If you haven't added real keys yet, the system works in **Demo Mode**:
- Simulates payment process
- No real money transaction
- Good for development

### 4.2 Test Mode (With Test Keys)
Once you add test keys:

#### Test Card Details:
```
Card Number:  4111 1111 1111 1111
CVV:          Any 3 digits (e.g., 123)
Expiry:       Any future date (e.g., 12/25)
Name:         Any name
```

#### Test UPI:
```
UPI ID: success@razorpay
```

#### Test Wallets:
- Select any wallet
- Use test credentials provided in Razorpay dashboard

### 4.3 Testing Flow
1. Browse to a **paid course**
2. Click **"Buy Now"**
3. Payment modal opens
4. Click **"Pay Securely with Razorpay"**
5. Razorpay checkout opens
6. Use test card details above
7. Click **"Pay"**
8. Payment succeeds → Enrollment created
9. Access course content

---

## 📊 Step 5: Monitor Transactions

### 5.1 Dashboard Access
1. Login to [Razorpay Dashboard](https://dashboard.razorpay.com/)
2. Go to **"Transactions"** section
3. View all payment attempts

### 5.2 Transaction Details
For each transaction, you can see:
- Payment ID
- Order ID
- Amount
- Status (Success/Failed)
- Customer details
- Timestamp

### 5.3 Database Records
Check `payments_payment` table in Django admin:
```python
# Access via: http://localhost:8000/admin/
- View all payment records
- Filter by status
- See user and course details
```

---

## 🔒 Step 6: Security Features

### 6.1 Signature Verification
The system automatically verifies Razorpay signatures to prevent tampering:

```python
# In payments/views.py
razorpay_client.utility.verify_payment_signature(params_dict)
```

### 6.2 CSRF Protection
All payment endpoints are CSRF protected:
```python
@csrf_exempt  # Only on verify_payment (Razorpay webhook)
```

### 6.3 User Authentication
All payment endpoints require login:
```python
@login_required
def create_order(request, course_id):
    ...
```

---

## 🎨 Step 7: Payment UI Features

### 7.1 Modal-Based Checkout
- Clean, modern payment modal
- Course details display
- Price breakdown
- Secure payment badge

### 7.2 Demo Mode Indicator
When using demo credentials:
```
🚧 DEMO MODE ACTIVE 🚧
You are using test credentials.
Click OK to simulate a successful payment.
```

### 7.3 Real Payment Flow
With real keys:
- Razorpay secure checkout opens
- Multiple payment options (Card, UPI, Wallet, Netbanking)
- Payment verification
- Success/Failure handling

---

## 📱 Step 8: Payment Flow Diagram

```
┌─────────────────────────────────────────────────────────┐
│ Student clicks "Buy Now" on Course Detail Page         │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ Payment Modal Opens (Shows price, course details)      │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ Student clicks "Pay Securely with Razorpay"            │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ Backend creates Razorpay order via API                 │
│ - POST /payments/create-order/<course_id>/             │
│ - Returns order_id, amount, key_id                     │
└─────────────────────────────────────────────────────────┘
                        ↓
        ┌───────────────┴───────────────┐
        │                               │
    DEMO MODE                      LIVE MODE
        │                               │
        ↓                               ↓
┌──────────────────┐           ┌───────────────────┐
│ Show Confirm Box │           │ Razorpay Checkout │
│ Simulate Payment │           │ Opens (Secure)    │
└──────────────────┘           └───────────────────┘
        │                               │
        ↓                               ↓
┌──────────────────┐           ┌───────────────────┐
│ Demo Enrollment  │           │ Student Pays with │
│ API Call         │           │ Card/UPI/Wallet   │
└──────────────────┘           └───────────────────┘
        │                               │
        ↓                               ↓
        └───────────────┬───────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ Backend verifies payment signature                      │
│ - POST /payments/verify-payment/                        │
│ - Checks Razorpay signature validity                    │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ Create Enrollment Record in Database                    │
│ Update Payment Status to "completed"                    │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ Redirect to Success Page                                │
│ Show congratulations message                            │
│ Student can now access course                           │
└─────────────────────────────────────────────────────────┘
```

---

## 🛠️ Step 9: Troubleshooting

### Issue 1: "Authentication failed"
**Solution**: Check if API keys are correct in settings.py

### Issue 2: Payment not creating enrollment
**Solution**: Check Django logs for errors in `verify_payment` view

### Issue 3: Razorpay checkout not opening
**Solution**: Ensure Razorpay checkout.js is loading (check browser console)

### Issue 4: Signature verification failed
**Solution**: Make sure Key Secret is correct and not modified

### Issue 5: Demo mode when you want live mode
**Solution**: Replace test keys with live keys in settings.py

---

## 📋 Step 10: Checklist

### Development (Test Mode)
- [ ] Created Razorpay account
- [ ] Enabled Test Mode
- [ ] Generated Test API Keys
- [ ] Updated settings.py with test keys
- [ ] Tested payment with test card
- [ ] Verified enrollment creation
- [ ] Checked transaction in dashboard

### Production (Live Mode)
- [ ] Completed KYC verification
- [ ] Switched to Live Mode
- [ ] Generated Live API Keys
- [ ] Updated settings.py with live keys
- [ ] Used environment variables for keys
- [ ] Tested real payment
- [ ] Set up webhook (optional)
- [ ] Configured email notifications

---

## 💡 Additional Features

### Webhooks (Optional)
Set up webhooks to receive payment notifications:

1. In Razorpay Dashboard → **Webhooks**
2. Add webhook URL: `https://yourdomain.com/payments/webhook/`
3. Select events: `payment.captured`, `payment.failed`
4. Copy webhook secret
5. Implement webhook handler in Django

### Refunds
To issue refunds:
```python
razorpay_client.payment.refund(payment_id, {
    'amount': amount_in_paise,
    'notes': {'reason': 'Course cancellation'}
})
```

### Partial Payments
Enable EMI or partial payments in Razorpay dashboard settings.

---

## 📞 Support

### Razorpay Support
- Email: support@razorpay.com
- Docs: https://razorpay.com/docs/
- Discord: https://razorpay.com/discord

### Django Project
- Check `payments/views.py` for payment logic
- Check `payments/models.py` for payment data model
- Check browser console for JavaScript errors

---

## 🎓 Summary

You now have a fully functional payment system with:

✅ **Secure Razorpay Integration**
✅ **Test Mode for Development**
✅ **Demo Mode Fallback**
✅ **Modal-Based Checkout**
✅ **Payment Verification**
✅ **Transaction Logging**
✅ **Automatic Enrollment**
✅ **Success/Failure Handling**

---

**Version**: 1.0  
**Last Updated**: October 18, 2025  
**Payment Gateway**: Razorpay  
**Framework**: Django 5.2
