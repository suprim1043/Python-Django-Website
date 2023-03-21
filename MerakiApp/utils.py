import json
from . models import *
import uuid


def create_id():
    now = datetime.datetime.now()
    return uuid4()




def CookieCart(request):
    total = 0
    orderitems = None
    order = None
    orderid = None
    product = Product.objects.all()
    product = product[:6]
    count = 0

    try:
        cart = json.loads(request.COOKIES['cart'])
        
    except:
        cart = {}

    orderitems = []
    orderoutofstock = []
    order = {'get_cart_total':0, 'get_cart_items': 0, 'get_cart_total_with_shipping':0}
    cartitems = order['get_cart_items']

    for i in cart:
        try:
            cartitems += cart[i]["quantity"]
            count = count+1
       
            product = Product.objects.get(productid = str(i))
            if product.product_name.remainingquantity != 0:


                ordertotal = (product.price * cart[i]["quantity"])
                order['get_cart_total'] += ordertotal
                order['get_cart_items'] += cart[i]["quantity"]
                total += cart[i]["quantity"]
                order['get_cart_total_with_shipping'] = order['get_cart_total'] +100
            

                items = {
                    'product':{
                    'productid':product.productid,
                    'product_name':product.product_name,
                    'price':product.price,
                    'size':product.product_name.size,
                    'firstimage':product.firstimage,
                    'allowedquantity':product.allowedquantity
                    },
                    'quantity':cart[i]["quantity"],
                    'get_total':ordertotal,
                    'remainingquantity':product.product_name.remainingquantity
                }

                orderitems.append(items)

            
            else:
                
                items = {
                    'product':{
                    'productid':product.productid,
                    'product_name':product.product_name,
                    'price':product.price,
                    'size':product.product_name.size,
                    'firstimage':product.firstimage,
                    'allowedquantity':product.allowedquantity
                    },
                    'quantity':cart[i]["quantity"],
                    'get_total':product.price,
                    'remainingquantity':product.product_name.remainingquantity
                }

                orderitems.append(items)


            
        except:
            pass
    return {"total":total,"orderitems":orderitems,"order":order,"product":product}
