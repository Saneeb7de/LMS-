# 💳 Razorpay Integration - Quick Start

## 🚀 5-Minute Setup

### Step 1: Get API Keys (2 minutes)
1. Visit: https://razorpay.com → Sign Up
2. Login: https://dashboard.razorpay.com
3. Enable **Test Mode** (toggle at top)
4. Go to: **Settings → API Keys**
5. Click: **"Generate Test Key"**
6. Copy both keys:
   ```
   Key ID: rzp_test_XXXXXXXXXXXXX
   Key Secret: XXXXXXXXXXXXXXXXXXXXXXXX
   ```

### Step 2: Update Django Settings (1 minute)
Open `lms_platform/settings.py` (line ~145):
```python
# Replace these lines:
RAZORPAY_KEY_ID = 'your_razorpay_key_id'
RAZORPAY_KEY_SECRET = 'your_razorpay_key_secret'

# With your actual keys:
RAZORPAY_KEY_ID = 'rzp_test_XXXXXXXXXXXXX'
RAZORPAY_KEY_SECRET = 'XXXXXXXXXXXXXXXXXXXXXXXX'
```

### Step 3: Restart Server (30 seconds)
```bash
# Stop server (Ctrl+C)
# Start again
python manage.py runserver
```

### Step 4: Test Payment (1.5 minutes)
1. Go to: http://127.0.0.1:8000/courses/browse/
2. Click on any **PAID** course
3. Click **"Buy Now"**
4. Click **"Pay Securely with Razorpay"**
5. Use test card:
   ```
   Card: 4111 1111 1111 1111
   CVV:  123
   Date: 12/25
   Name: Test User
   ```
6. Click **"Pay"**
7. ✅ Success! You're enrolled!

---

## 🎯 Test Card Numbers

| Card Type | Number | CVV | Result |
|-----------|--------|-----|--------|
| Success | 4111 1111 1111 1111 | Any | Success |
| Success | 5555 5555 5555 4444 | Any | Success |
| Failure | 4000 0000 0000 0002 | Any | Declined |

**Expiry**: Any future date (e.g., 12/25)  
**CVV**: Any 3 digits (e.g., 123)  
**Name**: Any name

---

## 🔧 Current Payment Flow

### Demo Mode (Default - No Keys)
```
Buy Now → Confirm Dialog → Simulated Success → Enrolled
```

### Test Mode (With Test Keys)
```
Buy Now → Razorpay Checkout → Test Payment → Verified → Enrolled
```

### Live Mode (Production)
```
Buy Now → Razorpay Checkout → Real Payment → Verified → Enrolled
```

---

## 📍 File Locations

| Purpose | File | Line |
|---------|------|------|
| API Keys | `lms_platform/settings.py` | ~145 |
| Payment Views | `payments/views.py` | All |
| Payment Modal | `templates/courses/course_detail.html` | ~265 |
| Payment Model | `payments/models.py` | All |

---

## ✅ Quick Checklist

- [ ] Created Razorpay account
- [ ] Got Test API keys (Key ID & Secret)
- [ ] Updated settings.py with keys
- [ ] Restarted Django server
- [ ] Tested payment with test card
- [ ] Verified enrollment created
- [ ] Checked transaction in Razorpay Dashboard

---

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| Payment fails | Check if keys are correct in settings.py |
| "Authentication failed" | Keys might be wrong or not saved |
| Demo mode appearing | Keys not updated or server not restarted |
| Checkout not opening | Check browser console for errors |

---

## 📚 Full Documentation

See [`RAZORPAY_SETUP_GUIDE.md`](./RAZORPAY_SETUP_GUIDE.md) for complete details:
- Step-by-step setup
- Security features
- Webhooks
- Refunds
- Production deployment

---

## 🎓 URLs to Remember

| Purpose | URL |
|---------|-----|
| Razorpay Dashboard | https://dashboard.razorpay.com |
| Documentation | https://razorpay.com/docs |
| Test Cards | https://razorpay.com/docs/payments/payments/test-card-details/ |
| Support | support@razorpay.com |

---

**Ready in 5 Minutes!** 🚀
