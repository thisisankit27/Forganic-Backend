from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class paymentCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coupon = models.CharField(max_length=100, null=True, blank=True) #Make Foriegn key Later
    is_paid = models.BooleanField(default=False)
    razorpay_order_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self) -> str:
        return self.user.username