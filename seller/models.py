from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=150)
    business_address = models.TextField()
    payment_details = models.TextField( blank=True, null=True)
    wallet_balance = models.DecimalField(max_digits=10, decimal_places=2, default=200.00)
    profile_picture = models.ImageField(upload_to='seller_profiles/', blank=True, null=True)

    def __str__(self):
        return f"Seller: {self.business_name} ({self.user.username})" 

class Withdrawal(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('REJECTED', 'Rejected'),
    )

    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)


class Item(models.Model):

    item_image = models.ImageField(upload_to='item_image/')
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    @property
    def formatted_price(self):
        return "{:,.2f}".format(self.price)
    category = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField(default=1)
    is_sold = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Item: {self.title} - {self.category} - ${self.price} - {self.quantity} in stock - {'Sold:' if self.is_sold else 'Available'}"