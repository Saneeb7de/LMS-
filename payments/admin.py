from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'amount', 'payment_status', 'transaction_date')
    list_filter = ('payment_status', 'transaction_date')
    search_fields = ('user__username', 'course__title', 'razorpay_order_id', 'razorpay_payment_id')
    readonly_fields = ('transaction_date', 'updated_at')
