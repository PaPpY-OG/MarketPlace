from django.contrib import admin
from .models import Seller
from .models import Item

# Register your models here.
admin.site.register(Seller)
admin.site.register(Item)