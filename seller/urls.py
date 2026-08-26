from django.urls import path
from . import views

urlpatterns = [
    path('seller/signup/',views.sellerSIGNUP, name='sellerSign'),
    path('seller/login/', views.sellerLOG, name='sellerLog'),
    path("",views.landing_page, name='landpage'),
    path("sellerDash/", views.SellerDash, name='seller_Dash'),
    path('seller/profile/', views.profile, name='seller_profile'),
    path('seller/edit_profile/', views.edit_profile, name='sedit_profile'),
    path('seller/change_password/', views.change_password, name='schange_password'),
    path("createItem/", views.createItem, name='createItem'),
    path('Slogout/', views.Logout, name='Slogout'),
    path('view_items/', views.viewItems, name='viewItem'),
    path('editItem/<int:item_id>/', views.editItem, name='editItem'),
    path('deleteItem/<int:item_id>/', views.deleteItem, name='deleteItem'),
    path('seller_orders/', views.seller_orders, name='seller_orders'),
    path('update_order_status/<int:purchase_id>/', views.update_order_status, name='update_order_status'),
    path('withdraw_funds/', views.withdraw_funds, name='withdraw_funds')
]