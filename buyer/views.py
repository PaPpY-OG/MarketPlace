from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from seller.models import Item
from .models import Buyer, Purchase, Wishlist
from django.db.models import Q


# Create your views here.
def buyerSIGN(request: HttpRequest):
    error = None
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2 or len(password1) < 8 :
            error = 'ensure both passwords match and length is greater than 7'
        else : 
            try :
                user_exist = User.objects.filter(username = username).first()
                email_exist = User.objects.filter(email=email).first()
                if user_exist :
                    error = 'Username already taken'
                elif email_exist:
                    error = 'Email already registered'
                else:
                    user = User.objects.create_user(username = username, email = email, password=password1)
                    Buyer.objects.create(user=user)
                    user.save()
                    return redirect("buyersLogin")
            except Exception as e :
                error = str (e)
    return render(request,'signup2.html', {"error" : error})

def buyerLOG(request: HttpRequest):
    error,message = None, None
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not password or len(password) < 8 :
            return render(request, 'login2.html', {"error":True, "message":"password is required and must meet minimun length to login"})
        user_returned = authenticate(request, username=username, password=password)
        if not user_returned :
            return render(request, 'login2.html',{"error": True, "message": "Invalid Credentials"})
        login(request, user_returned)
        return redirect("buyerDash")
    
    return render(request, 'login2.html', {"error": error, "message": message})

@login_required(login_url='buyersLogin')
def buyerDash(request: HttpRequest):
    buyer = Buyer.objects.get(user=request.user)
    items = Item.objects.filter(is_sold=False).order_by('-created_at')

    #Search
    query = request.GET.get('q')
    if query:
        items = items.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(category__icontains=query)
        )

    #Category filter
    category = request.GET.get('category')
    if category:
        items = items.filter(category=category)

    return render(request, 'buyerDash.html', {
        'items': items,
        'buyer': buyer,
        'query': query,
        'category': category
    })

@login_required(login_url='buyersLogin')
def add_to_cart(request: HttpRequest, item_id):
    item = get_object_or_404(Item, id=item_id)
    buyer = Buyer.objects.get(user=request.user)

    # ensure cart is always a dict
    cart = request.session.get('cart', {})

    if isinstance(cart, list):
        cart = {}

    item_id = str(item_id)

    current_qty = cart.get(item_id, {}).get('qty', 0)

    # prevent exceeding stock
    if current_qty >= item.quantity:
        request.session['error'] = "You cannot add more than available stock"
        return redirect('buyerDash')

    if item_id in cart:
        cart[item_id]["qty"] += 1
    else:
        cart[item_id] = {
            "qty": 1
        }

    request.session['cart'] = cart
    request.session.modified = True

    request.session['success'] = "Added to cart"

    return redirect('buyerDash')

@login_required(login_url='buyersLogin')
def remove_from_cart(request: HttpRequest, item_id):
    item_id = str(item_id)

    cart = request.session.get('cart', {})

    if isinstance(cart, list):
        cart = {}

    if item_id in cart:
        if cart[item_id]["qty"] > 1:
            cart[item_id]["qty"] -= 1
        else:
            del cart[item_id]

        request.session['cart'] = cart
        request.session.modified = True

        request.session['success'] = "Item updated/removed from cart"

    return redirect('cart')
    
@login_required(login_url='buyersLogin')
def cart(request):
    buyer = Buyer.objects.get(user=request.user)

    cart = request.session.get('cart', {})

    items = []
    total = 0

    for item in Item.objects.filter(id__in=cart.keys()):
        item_id = str(item.id)
        qty = cart.get(item_id, {}).get('qty', 0)

        item.cart_qty = qty
        item.subtotal = item.price * qty

        total += item.subtotal
        items.append(item)

    return render(request, 'cart.html', { "buyer": buyer, "items": items, "total": total})

@login_required(login_url='buyersLogin')
def increase_qty(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    cart = request.session.get('cart', {})
    item_id = str(item_id)

    if isinstance(cart, list):
        cart = {}

    if item_id in cart:
        current_qty = cart[item_id].get('qty', 0)

        # prevent exceeding stock
        if current_qty >= item.quantity:
            request.session['error'] = "You cannot exceed available stock"
            return redirect('cart')

        cart[item_id]['qty'] += 1

        request.session['cart'] = cart
        request.session.modified = True

    return redirect('cart')

@login_required(login_url='buyersLogin')
def decrease_qty(request: HttpRequest, item_id):
    item_id = str(item_id)
    cart = request.session.get('cart', {})

    # safety check (in case old session format exists)
    if isinstance(cart, list):
        cart = {}

    if item_id in cart:
        current_qty = cart[item_id].get('qty', 0)

        current_qty -= 1

        if current_qty <= 0:
            del cart[item_id]
        else:
            cart[item_id]['qty'] = current_qty

        request.session['cart'] = cart
        request.session.modified = True

        request.session['success'] = "Cart updated"

    return redirect('cart')

@login_required(login_url='buyersLogin')
def wishlist_view(request):
    buyer = Buyer.objects.get(user=request.user)

    wishlist_items = Wishlist.objects.filter(buyer=buyer).select_related('item')

    return render(request, 'wishlist.html', {
        'wishlist_items': wishlist_items,
        'buyer': buyer
    })

@login_required(login_url='buyersLogin')
def add_to_wishlist(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    Wishlist.objects.get_or_create(buyer=request.user.buyer, item=item)
    return redirect('wishlist')

@login_required(login_url='buyersLogin')
def remove_wishlist(request, item_id):
    buyer = Buyer.objects.get(user=request.user)

    Wishlist.objects.filter(buyer=buyer, item_id=item_id).delete()

    return redirect('wishlist')

@login_required(login_url='buyersLogin')
def orderhistory(request):
    buyer = Buyer.objects.get(user=request.user)
    purchases = Purchase.objects.filter(buyer=buyer).order_by('-purchase_date')

    return render(request, 'orderhistory.html', {'purchases': purchases,'buyer': buyer})

@login_required(login_url='buyersLogin')
def checkout(request):
    buyer = Buyer.objects.get(user=request.user)
    cart = request.session.get('cart', {})

    # Get all items in cart
    item_ids = cart.keys()
    items = Item.objects.filter(id__in=item_ids)

    # Calculate total properly using quantities
    total = 0

    for item in items:
        qty = cart[str(item.id)]['qty']
        total += item.price * qty

    if request.method == "POST":

        payment_method = request.POST.get('payment_method')

        if payment_method not in ['Bitcoin', 'Cash Transfer']:
            return render(request, 'checkout.html', {'buyer': buyer,'total': total, 'error': 'Please select a valid payment method.'})

        if buyer.wallet_balance < total:
            return render(request, 'checkout.html', {'buyer': buyer,'total': total,'error': 'Insufficient balance.'})

        # Process each cart item
        for item in items:

            qty = cart[str(item.id)]['qty']

            # Reduce stock
            item.quantity -= qty

            # Mark sold only when stock reaches zero
            if item.quantity == 0:
                item.is_sold = True

            item.save()

            # Credit seller
            seller = item.seller
            seller.wallet_balance += item.price * qty
            seller.save()

            # Save purchase record
            Purchase.objects.create(buyer=buyer, item=item, amount=item.price * qty, quantity=qty)

        # Deduct buyer balance
        buyer.wallet_balance -= total
        buyer.save()

        # Empty cart
        request.session['cart'] = {}
        request.session.modified = True

        return redirect(request, 'checkout.html', {'buyer': buyer,'total': 0,'success': f'Purchase successful via {payment_method}!'})
    return render(request, 'checkout.html', {'buyer': buyer,'total': total})

@login_required(login_url='buyersLogin')
def profile(request):
    buyer = Buyer.objects.get(user=request.user)
    purchase_count = Purchase.objects.filter(buyer=buyer).count()

    return render(request, 'profile.html', { 'buyer': buyer, 'purchase_count': purchase_count,})

@login_required(login_url='buyersLogin')
def edit_profile(request):
    buyer = Buyer.objects.get(user=request.user)

    if request.method == "POST":

        username = request.POST.get('username')
        picture = request.FILES.get('profile_picture')

        request.user.username = username
        request.user.save()

        if picture:
            buyer.profile_picture = picture

        buyer.save()

    return redirect('profile')

@login_required(login_url='buyersLogin')
def change_password(request):
    error = None
    success = None

    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password or len(new_password) < 8:
            error = 'ensure both passwords match and length is greater than 7'
        else : 
            user = authenticate(request, username=request.user.username, password=current_password)
            if user:
                user.set_password(new_password)
                user.save()
                success = 'Password changed successfully'                
            else:
                error = 'Current password is incorrect'
    return render(request, 'profile.html', {'error': error, 'success': success})

@login_required(login_url='buyersLogin')
def Logout(request:HttpRequest):
    logout(request)
    return redirect("buyersLogin")
