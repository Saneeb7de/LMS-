# 💳 Razorpay Integration - Testing Guide

## ✅ Configuration Complete

### **Your Razorpay Keys (Test Mode)**
```
Key ID:     rzp_test_RUuGPDMr5Tpljw
Key Secret: tU97fVv8kmJ1A2c73Rq9L1XH
Status:     ✅ Configured in settings.py
Mode:       Test Mode
```

---

## 🧪 Testing Instructions

### **1. Test Payment Flow (With Real Razorpay)**

#### **Step 1: Browse Courses**
1. Visit: http://127.0.0.1:8000/courses/browse/
2. Find a **PAID** course (shows price badge)
3. Click on the course

#### **Step 2: Enroll**
1. Click **"Buy Now"** button
2. You'll be redirected to enrollment page
3. See course details and price

#### **Step 3: Pay with Razorpay**
1. Click **"Pay Securely"** button
2. **Razorpay Checkout** window opens
3. You'll see:
   - Course name
   - Amount to pay
   - Payment options (Card, UPI, Wallet, etc.)

#### **Step 4: Use Test Card**
```
Card Number:  4111 1111 1111 1111
CVV:          Any 3 digits (e.g., 123)
Expiry Date:  Any future date (e.g., 12/25)
Cardholder:   Any name
```

#### **Step 5: Complete Payment**
1. Click **"Pay"** in Razorpay
2. Payment processes
3. Signature verification happens
4. Enrollment created
5. Redirected to **Success Page**

#### **Step 6: Access Course**
1. Click **"Go to Course"**
2. Start learning!

---

## 🎯 All Available Test Cards

### **Success Cards:**
```
Visa:           4111 1111 1111 1111
Mastercard:     5555 5555 5555 4444
Rupay:          6522 1111 1111 1234
```

### **Decline/Fail Cards:**
```
Declined:       4000 0000 0000 0002
Expired:        4000 0000 0000 0069
CVV Fail:       4000 0000 0000 0127
```

### **Test UPI:**
```
Success:        success@razorpay
Failure:        failure@razorpay
```

### **Test Wallets:**
- Any wallet will work in test mode
- Payment succeeds automatically

---

## 📊 API Endpoints Being Tested

### **1. Create Order API**
**Endpoint:** `POST /payments/create-order/<course_id>/`

**Request:**
```json
{
  "method": "POST",
  "headers": {
    "X-CSRFToken": "...",
    "Content-Type": "application/json"
  }
}
```

**Expected Response (Success):**
```json
{
  "success": true,
  "order_id": "order_XXXXXXXXXXXX",
  "amount": 299900,  // in paise
  "currency": "INR",
  "key_id": "rzp_test_RUuGPDMr5Tpljw"
}
```

**Expected Response (Error):**
```json
{
  "success": false,
  "message": "Error description"
}
```

---

### **2. Verify Payment API**
**Endpoint:** `POST /payments/verify-payment/`

**Request:**
```json
{
  "razorpay_payment_id": "pay_XXXXXXXXXXXX",
  "razorpay_order_id": "order_XXXXXXXXXXXX",
  "razorpay_signature": "XXXXXXXXXXXX"
}
```

**Expected Response (Success):**
```json
{
  "success": true,
  "message": "Payment successful! You are now enrolled.",
  "course_id": 18
}
```

**Expected Response (Failure):**
```json
{
  "success": false,
  "message": "Payment verification failed"
}
```

---

## 🔍 Verification Steps

### **1. Check Razorpay Dashboard**
1. Login to: https://dashboard.razorpay.com
2. Go to **Transactions**
3. You should see your test payment
4. Check:
   - Order ID
   - Payment ID
   - Amount
   - Status (Success/Failed)
   - Customer details

### **2. Check Django Database**
Open Django admin: http://127.0.0.1:8000/admin/

#### **Payments Table:**
```
payments_payment
├── razorpay_order_id
├── razorpay_payment_id
├── razorpay_signature
├── amount
├── payment_status (should be 'completed')
├── user
└── course
```

#### **Enrollments Table:**
```
courses_enrollment
├── user
├── course
├── progress (starts at 0)
├── enrolled_at
└── is_active (should be True)
```

### **3. Test Course Access**
1. After payment, go to dashboard
2. Course should appear in "In Progress"
3. Click "Continue Learning"
4. You should be able to access all modules

---

## 🧪 Complete Test Scenario

### **Scenario: New Student Purchases Course**

```
┌─────────────────────────────────────────┐
│ 1. Student browses courses              │
│    URL: /courses/browse/                │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ 2. Clicks on paid course                │
│    URL: /courses/<id>/                  │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ 3. Clicks "Buy Now"                     │
│    URL: /payments/enroll/<id>/          │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ 4. Clicks "Pay Securely"                │
│    API: POST /payments/create-order/    │
│    Response: order_id, amount, key_id   │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ 5. Razorpay Checkout Opens              │
│    - Shows course name                  │
│    - Shows amount                       │
│    - Payment options visible            │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ 6. Enters test card details             │
│    Card: 4111 1111 1111 1111            │
│    CVV: 123                             │
│    Expiry: 12/25                        │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ 7. Clicks "Pay"                         │
│    Razorpay processes payment           │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ 8. Payment Success Callback             │
│    Returns: payment_id, order_id, sig   │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ 9. Verify Payment                       │
│    API: POST /payments/verify-payment/  │
│    Checks signature validity            │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ 10. Create Enrollment                   │
│     - Payment marked as 'completed'     │
│     - Enrollment record created         │
│     - User can now access course        │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ 11. Success Page                        │
│     URL: /payments/success/<id>/        │
│     Shows congratulations message       │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ 12. Access Course                       │
│     URL: /courses/<id>/learn/           │
│     Student can now watch videos        │
└─────────────────────────────────────────┘
```

---

## 🐛 Troubleshooting

### **Issue 1: "Razorpay Checkout not opening"**
**Solution:**
- Check browser console for errors
- Ensure `checkout.js` is loaded
- Verify API keys are correct

### **Issue 2: "Payment verification failed"**
**Solution:**
- Check if `RAZORPAY_KEY_SECRET` is correct
- Signature mismatch means secret is wrong
- Check Django logs for exact error

### **Issue 3: "Order creation failed"**
**Solution:**
- Check if Razorpay keys are valid
- Ensure Test Mode is enabled
- Check network tab for API response

### **Issue 4: "Enrollment not created"**
**Solution:**
- Check if payment was verified successfully
- Check Django admin → Payments table
- Ensure user is authenticated

---

## 📝 Test Checklist

Use this checklist to verify everything works:

### **Before Testing:**
- [ ] Razorpay keys configured in `settings.py`
- [ ] Server is running
- [ ] You have a student account
- [ ] At least one paid course exists

### **During Testing:**
- [ ] Browse courses page loads
- [ ] Can click on paid course
- [ ] Buy Now button works
- [ ] Enrollment page shows correct price
- [ ] Pay Securely button opens Razorpay
- [ ] Razorpay checkout displays
- [ ] Can enter test card details
- [ ] Payment processes successfully
- [ ] Signature verification works
- [ ] Redirected to success page

### **After Testing:**
- [ ] Payment visible in Razorpay Dashboard
- [ ] Payment record in Django admin
- [ ] Enrollment record created
- [ ] Can access course content
- [ ] Course shows in dashboard
- [ ] Progress tracking works

---

## 🔒 Security Checks

### **What's Being Verified:**
1. ✅ **Signature Verification**: Prevents payment tampering
2. ✅ **CSRF Protection**: All POST requests protected
3. ✅ **Authentication**: Only logged-in users can pay
4. ✅ **Duplicate Prevention**: Can't pay twice for same course
5. ✅ **Amount Validation**: Server controls the price
6. ✅ **SSL/HTTPS**: In production, all traffic encrypted

---

## 🎓 Expected Results

### **Successful Payment Flow:**
```
Time: ~30-45 seconds total
Steps: 12 total
APIs Called: 2 (create-order, verify-payment)
Database Writes: 2 (Payment, Enrollment)
Final Status: Student enrolled and can access course
```

### **Database State After Success:**
```sql
-- Payment Record
INSERT INTO payments_payment (
    user_id, course_id, amount,
    razorpay_order_id, razorpay_payment_id, razorpay_signature,
    payment_status, created_at
) VALUES (
    1, 18, 2999.00,
    'order_XXXX', 'pay_XXXX', 'sig_XXXX',
    'completed', NOW()
);

-- Enrollment Record
INSERT INTO courses_enrollment (
    user_id, course_id, progress,
    enrolled_at, is_active
) VALUES (
    1, 18, 0,
    NOW(), TRUE
);
```

---

## 📊 Monitoring

### **Real-time Logs:**
Watch Django console for:
```
POST /payments/create-order/18/ HTTP/1.1 200 197
POST /payments/verify-payment/ HTTP/1.1 200 XX
GET /payments/success/18/ HTTP/1.1 200 XXXXX
```

### **Razorpay Dashboard:**
- Go to Transactions
- Filter by date: Today
- Check payment status
- View customer details

---

## ✅ Success Criteria

Your payment integration is working correctly if:

1. ✅ Razorpay checkout opens
2. ✅ Test card payment succeeds
3. ✅ Signature verification passes
4. ✅ Enrollment is created
5. ✅ Student can access course
6. ✅ Transaction visible in Razorpay Dashboard
7. ✅ Payment record in Django database

---

## 🚀 Next Steps

Once testing is complete:

### **For Production:**
1. Complete Razorpay KYC verification
2. Switch to **Live Mode** in dashboard
3. Generate **Live API Keys**
4. Update `settings.py` with live keys
5. Enable HTTPS on your domain
6. Test with small real payment
7. Go live! 🎉

---

**Test Mode Active:** ✅  
**Integration Status:** Ready to Test  
**Documentation:** Complete  

Start testing at: http://127.0.0.1:8000/courses/browse/
