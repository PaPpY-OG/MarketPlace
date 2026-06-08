from django.shortcuts import redirect
from seller.models import Seller

def seller_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("/seller/login")
        if not Seller.objects.filter(user=request.user).exists():
            return redirect("/buyer/login")
        return view_func(request, *args, **kwargs)
    return wrapper