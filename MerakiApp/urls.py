from django.urls import path, URLPattern
from . import views
from .models import *
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.Products, name = 'products'),
    path('bestsellers', views.mainpage, name = 'home'),
    path('login',views.login, name = 'login'),
    path('logout', views.logout, name = 'logout'),
    path('profile',views.profile, name = 'profile'),
    path('cart',views.cart, name = 'cart'),
    path('checkout',views.checkout, name = 'checkout'),
    path('payment',views.payment, name = 'payment'),
    path('shippinginfo',views.shippinginfo, name = 'shippinginfo'),
    path('orderconfirmed',views.orderconfirmed, name = 'orderconfirmed'),
    path('ordertracking', views.ordertracking, name = "order"),
    path('updateitem',views.UpdateItem, name = 'update_items'),
    path('cartupdate',views.cartupdate, name = 'cartupdate'),
    path('register',views.register, name = 'register'),
    path('products',views.Products, name = 'products'),
    path('search', views.Search, name = 'search'),
    path('productdescription/search', views.Search, name = 'search'),
    path('category/search', views.Search, name = 'search'),
    path('category/<str:category>',views.CategoryName),
    path('productdescription/<uuid:productid>',views.productdetails, name = 'productdescription'), 
    path('reset', auth_views.PasswordResetView.as_view(template_name = 'reset.html'), name = "reset_password"),
    path('resetsent', auth_views.PasswordResetDoneView.as_view(template_name = 'resetsent.html'), name = "password_reset_done"),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name = 'resetform.html'), name = "password_reset_confirm"),
    path('resetcomplete', auth_views.PasswordResetCompleteView.as_view(template_name = 'resetcomplete.html'), name = "password_reset_complete"),
]