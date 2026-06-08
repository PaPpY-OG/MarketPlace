from django.shortcuts import redirect
from buyer.models import Buyer

def buyer_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("/buyer/login")
        if not Buyer.objects.filter(user=request.user).exists():
            return redirect("/seller/login")
        return view_func(request, *args, **kwargs)
    return wrapper