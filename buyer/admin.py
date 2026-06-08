from django.contrib import admin
from .models import Buyer, Cart, Wishlist, Purchase

# Register your models here.
admin.site.register(Buyer)
admin.site.register(Purchase)
admin.site.register(Cart)
admin.site.register(Wishlist)