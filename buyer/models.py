from django.db import models
from django.contrib.auth.models import User
from seller.models import Item
from random import randint

# Create your models here.

def generateOrderNumber():
    """a simple function to generate a random order number"""
    return str(randint(10000000, 99999999))

class Buyer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    wallet_balance = models.DecimalField(max_digits=10, decimal_places=2, default=5000000.00)
    profile_picture = models.ImageField(upload_to='buyer_profiles/', blank=True,null=True,)

    def __str__(self):
        return f"Buyer: {self.user.username}"

class Purchase(models.Model):

    STATUS_CHOICES = (
        ('PROCCESSING', 'Processing'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
    )

    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=20, unique=True, default=generateOrderNumber)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantity = models.IntegerField(default=1)
    purchase_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='PROCCESSING')


    def __str__(self):
        return f"Purchase: {self.item.title} by {self.buyer.user.username} on {self.purchase_date}"

class Cart(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

class Wishlist(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Wishlist: {self.item.title} by {self.buyer.user.username}"