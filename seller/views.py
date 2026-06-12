from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import Item, Seller
from django.db.models import Q


# Create your views here.
def landing_page(request):
    query = request.GET.get('q')

    featured_products = Item.objects.filter(is_sold=False)

    if query:
        featured_products = featured_products.filter(
            Q(title__icontains=query) |
            Q(category__icontains=query) |
            Q(description__icontains=query)
        ).order_by('-created_at')

    else:
        featured_products = featured_products.order_by('-created_at')[:4]

    return render(request,'landing.html',{'featured_products': featured_products,'query': query})

def sellerSIGNUP(request: HttpRequest):
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
                email_exist = User.objects.filter(email = email).first
                if user_exist :
                    error = 'Username has been taken'
                elif email_exist :
                    error = 'Email already registered'
                else:
                    user = User.objects.create_user( username=username, email=email, password=password1)
                    Seller.objects.create(user=user)
                    user.save()
                    return redirect("sellerLog")
            except Exception as e :
                error = str (e)
    return render(request,'signup1.html', {"error" : error})

def sellerLOG(request: HttpRequest):
    error,message = None, None
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not password or len(password) < 8 :
            return render(request, 'login1.html', {"error":True, "message":"password is required and must meet minimun length to login"})
        user_returned = authenticate(request, username=username, password=password)
        if not user_returned :
            return render(request, 'login1.html',{"error": True, "message": "Invalid Credentials"})
        login(request, user_returned)
        return redirect("seller_Dash")
    
    return render(request, 'login1.html', {"error": error, "message": message})

@login_required(login_url='sellerLog')
def createItem(request: HttpRequest):
    error, message = None, None
    if request.method == "POST":
        item_image = request.FILES.get('item_image')
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        category = request.POST.get('category')
        is_sold = request.POST.get('is_sold') == 'on'
        #first check if item exist
        try :
                item_exist = Item.objects.filter(title = title).first()
                if item_exist :
                    error = 'Item already exists for this title'
                else:
                    price = float(price)
                    seller = Seller.objects.get(user=request.user)
                    item = Item.objects.create(item_image=item_image, title=title, description=description, price=price, quantity=quantity, category=category, 
                    is_sold=is_sold, seller=seller)

                    item.save()
                    message = "Item created successfully"
                    return redirect("seller_Dash")
        except Exception as e :
                error = str (e)
    return render(request, 'createItems.html', {"error":error, "message":message})

@login_required(login_url='sellerLog')
def SellerDash(request: HttpRequest):
    seller = Seller.objects.get(user=request.user)
    total_items = Item.objects.filter(seller=seller).count()
    sold_items = Item.objects.filter(seller=seller, is_sold=True).count()
    return render(request, 'sellerDash.html', {'seller': seller, 'total_items': total_items, 'sold_items': sold_items})

@login_required(login_url='sellerLog')
def profile(request: HttpRequest):
    seller = Seller.objects.get(user=request.user)
    sales_count = Item.objects.filter(seller=seller, is_sold=True).count()
    return render(request, 'Sprofile.html', {'seller': seller, 'sales_count': sales_count})

@login_required(login_url='sellerLog')
def edit_profile(request):
    seller = Seller.objects.get(user=request.user)

    if request.method == "POST":

        username = request.POST.get('username')
        picture = request.FILES.get('profile_picture')

        request.user.username = username
        request.user.save()

        if picture:
            seller.profile_picture = picture

        seller.save()

    return redirect('seller_profile')

@login_required(login_url='sellerLog')
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
    return render(request, 'Sprofile.html', {'error': error, 'success': success})

@login_required(login_url='sellerLog')
def Logout(request:HttpRequest):
    logout(request)
    return redirect("sellerLog")

@login_required(login_url='sellerLog')
def viewItems(request):
    seller = Seller.objects.get(user=request.user)
    items = Item.objects.filter(seller=seller).order_by('-id')  # newest first
    return render(request, 'view_items.html', {'items': items, 'seller':seller})


@login_required(login_url='sellerLog')
def editItem(request, item_id):
    item = get_object_or_404(Item, id=item_id, seller__user=request.user)

    if request.method == "POST":
        item_image = request.FILES.get('item_image')
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        category = request.POST.get('category')

        try:
            item.title = title
            item.description = description
            item.price = float(price)
            item.quantity = int(quantity)
            item.category = category

            if item_image:
                item.item_image = item_image

            item.is_sold = item.quantity <= 0
            item.save()

        except ValueError:
            pass  # optionally log error

    return redirect('viewItem')

@login_required(login_url='sellerLog')
def deleteItem(request, item_id):
    item = get_object_or_404(Item, id=item_id, seller__user=request.user)
    item.delete()
    return redirect('viewItem')