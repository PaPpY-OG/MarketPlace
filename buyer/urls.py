from django.urls import path
from . import views

urlpatterns = [
    path('buyer/signup/',views.buyerSIGN,name='buyerSign'),
    path('buyer/login/',views.buyerLOG, name='buyersLogin'),
    path('buyerDash/', views.buyerDash, name='buyerDash'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('add_to_cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('increase_qty/<int:item_id>/', views.increase_qty, name='increase_qty'),
    path('decrease_qty/<int:item_id>/', views.decrease_qty, name='decrease_qty'),
    path('cart/', views.cart, name='cart'),
    path('add_to_wishlist/<int:item_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove_wishlist/<int:item_id>/', views.remove_wishlist, name='remove_wishlist'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('orderhistory/', views.orderhistory, name='orderhistory'),
    path('checkout/', views.checkout, name='checkout'),
    path('buyer/logout/', views.Logout, name='Blogout')
]
