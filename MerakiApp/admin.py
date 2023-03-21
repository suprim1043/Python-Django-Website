from django.contrib import admin
from .models import *
from django.contrib.auth.models import User
import django.apps
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class block(admin.ModelAdmin):
    list_display = ('email', 'userid','first_name', 'last_name', 'is_active','last_login', 'date_joined', 'is_staff' )
class order(admin.ModelAdmin):
    list_display = ('customer','date_ordered','complete','orderid','status','ordertotal', "paymentstatus","paymentmethod","specialinstructions")
class orderitems(admin.ModelAdmin):
    list_display = ('product','order','quantity','date_added')

class shippinglist(admin.ModelAdmin):
    list_display = ('customer', 'order','address','city','contactnumber','alternatenumber','date_added')
class customerlist(admin.ModelAdmin):
    list_display = ('user', 'name', 'email')

admin.site.register(Customer, customerlist)
admin.site.register(myuser, block)
admin.site.register(Homepage_Slider)
admin.site.register(Order,order)
admin.site.register(OrderItem,orderitems)
admin.site.register(Shipping,shippinglist)
admin.site.register(Category)
admin.site.register(BestSellers)
admin.site.register(ContactModel)


class StockList(admin.ModelAdmin):
    list_display = ('product_name','quantity','size','remainingquantity','date','uploadedby')

class ProductList(admin.ModelAdmin):
    list_display = ('product_name','name','price','dateadded','rate','views')

class ReviewList(admin.ModelAdmin):
    list_display = ('ProductName','Name','Email','Date','Rating')


admin.site.register(Stock,StockList)
admin.site.register(Product,ProductList)
admin.site.register(Reviews,ReviewList)



