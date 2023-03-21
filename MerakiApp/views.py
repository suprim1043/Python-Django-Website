from django.shortcuts import render
from django.urls import resolve

from .models import *
from .forms import HomepageForm,UserForm,ContactForm,ReviewForm
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as log_in, logout as log_out
from django.contrib.auth import get_user_model
from PIL import Image
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.db import IntegrityError
User = get_user_model()
import math
import json
import random
from .utils import CookieCart


# Create your views here.
orderuniqueid = str(uuid4())


def cartupdate(request):
    pass


def mainpage(request):
    total = 0
    orderitems = None

    if request.user.is_authenticated:
        customer = request.user
        orderitems = None
        order = None
        try:
            order = Order.objects.get(customer__user__email = customer, complete = False)
            orderitems = order.orderitem_set.all()
            total = order.get_cart_items
   
        except:
            pass
            
        if request.method == "POST":
            form = ContactForm(request.POST)
            if form.is_valid():
                    ContactModel.Userid = request.POST.get("Userid")
                    ContactModel.FullName = request.POST.get("FullName")
                    ContactModel.Email = request.POST.get("Email")
                    email = request.POST.get("Email")
                    ContactModel.Query = request.POST.get("Query")
                    form.save()
                    messages.info(request,f"Dear {request.user.first_name}, Your Query has been successfully submitted. One of our reprensetative will contact you on the email you provided: {email}")
        else:
            pass
    
    else:
        CookieData = CookieCart(request)
        orderitems = CookieData['orderitems']
        order = CookieData['order']
        total = CookieData['total']
        print(orderitems)

      
 
        if request.method == "POST":
            form = ContactForm(request.POST)
            if form.is_valid():
                    fullname = request.POST.get("FullName")
                    ContactModel.Userid = request.POST.get("Userid")
                    ContactModel.FullName = request.POST.get("FullName")
                    ContactModel.Email = request.POST.get("Email")
                    email = request.POST.get("Email")
                    ContactModel.Query = request.POST.get("Query")
                    form.save()
                    messages.info(request,f"Dear {fullname}, Your Query has been successfully submitted. One of our reprensetative will contact you on the email you provided: {email}")
        else:
            pass



    form = ContactForm()
    category = Category.objects.all()



    context = {"total":total,"orderitems": orderitems, "data": list(Homepage_Slider.objects.filter(Page=1)),"data2":list(Homepage_Slider.objects.filter(Page=2)),"data3":list(Homepage_Slider.objects.filter(Page=3)),"user":request.user,"bestsellers":BestSellers.objects.all(),"products":Product.objects.all(),"form":form,"name":request.POST.get("FullName"),"email":request.POST.get("Email"),"category":category}
    return render(request, "main.html", context)


def homepage(request):
     
        form = HomepageForm()       
        if request.method == "POST":
            form = HomepageForm(request.POST,request.FILES)
            if form.is_valid():
                form.save()

        form = HomepageForm()        
        context = {"form":form}

        return render(request, "homepage.html", context)


def login(request):
    form = AuthenticationForm()
    if request.user.is_authenticated:
        return redirect('products')

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        request.POST.get('username')
        user = authenticate(request, username = username, password = password)

        if user is not None:
            log_in(request, user)
            return redirect('register')
        else:
            messages.info(request, "Username or Password is incorrect")


    context = {"form":form}
    return render(request,"login.html",context)

def logout(request):
    log_out(request)
    return redirect('products')


def register(request):
  

    form = UserForm()
    if request.user.is_authenticated:
        return redirect('products')
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            try:
                instance =  form.save(commit = False)
                instance.save()
                log_in(request,instance)
                return redirect('products')
                
            except: 
                email = form.data['email']
                messages.error(request,f"{email} is already registered in the database.")
        else:
            password1 = form.data['password1']
            password2 = form.data['password2']
            email = form.data['email']
        for msg in form.errors.as_data():
                if msg == 'password2' and password1 == password2:
                    messages.error(
                        request, f"Selected password: {password1} is not strong enough.")
                elif msg == 'password2' and password1 != password2:
                    messages.error(
                        request, f"Password: '{password1}' and Confirmation Password: '{password2}' do not match.")

                elif msg == 'email':
                    messages.error(
                        request, f"The email address '{email}' is already taken.") 
    context = {"form":form}
    return render(request, "register.html",context)




def Products(request):
    total = 0
    if request.user.is_authenticated:
        customer = request.user
        orderitems = None
        order = None
        try:
            order = Order.objects.get(customer__user__email = customer, complete = False)
            orderitems = order.orderitem_set.all()
            total = order.get_cart_items
   
        except:
            pass
    
    else:
        CookieData = CookieCart(request)
        orderitems = CookieData['orderitems']
        order = CookieData['order']
        total = CookieData['total']

       
  
    products = Product.objects.all()
    length = len(products)
    boxcontent = "Sort"




    if request.method == "GET":
        try:
            answer = request.GET['query']
        except:
            pass
        
    try:
        if answer == "SortByPricedesc":
            products = Product.objects.all().order_by('-price')
            boxcontent = "Sort By Price: High To Low"
        elif answer == "SortByPrice":
            products = Product.objects.all().order_by('price')
            boxcontent = "Sort By Price: Low To High"
        elif answer == "SortByBrand":
            products = Product.objects.all().order_by('product_name')
            boxcontent = "Sort By Brand"
        elif answer == "SortByDateAdded":
            products = Product.objects.all().order_by('-dateadded')
            boxcontent = "Sort By Date Added"
    except:
        pass

  



    context = {"products":products, "number":length,"boxcontent":boxcontent,"total":total}
    
    return render(request, "products.html", context)

def Search(request):
    total = 0
    if request.user.is_authenticated:
        customer = request.user
        orderitems = None
        order = None
        try:
            order = Order.objects.get(customer__user__email = customer, complete = False)
            orderitems = order.orderitem_set.all()
            total = order.get_cart_items
        except:
            pass
    
    else:
        CookieData = CookieCart(request)
        orderitems = CookieData['orderitems']
        order = CookieData['order']
        total = CookieData['total']

       
    objcount = 0
    randomobj = []
    bestsellers = BestSellers.objects.all()

    randomselect = Product.objects.all()
    for obj in randomselect:
        randomobj.append(obj)
    objcount = len(randomobj)

    
    rand = random.sample(randomobj,objcount)
    rand = rand[:6]

    query = request.GET['query']
    product = Product.objects.filter(product_name__product_name__icontains=query)

    context = {"product": product,"searchdata":query,"count":len(product),"bestseller":rand,"total":total}
    return render(request, "searchpage.html",context)

def cart(request):
    total = 0
    orderitems = None
    order = None
    orderid = None
    product = Product.objects.all()
    product = product[:6]
    count = 0
   


    if request.user.is_authenticated:
        customer = request.user
        try:
            order = Order.objects.get(customer__user__email = customer, complete = False)
            orderitems = order.orderitem_set.all()
            total = order.get_cart_items
           
        except:
            pass
        context = {"total":total,"orderitems":orderitems,"order":order,"product":product}
        return render(request, "authenticatedcart.html",context)
    
    else:
        CookieData = CookieCart(request)

        orderitems = CookieData['orderitems']
        order = CookieData['order']
        total = CookieData['total']
        for items in orderitems:
            count = count + 1
        



    

    context = {"total":total,"orderitems":orderitems,"order":order,"product":product,"orderuniqueid":orderuniqueid, "count":count}
 
    return render(request, "cart.html",context) 



def checkout(request):
    orderitems = None
    order = None
    ship = None
    allship = None
    orderid = None
    customer = None
    shiar = [] 
    orderitemss = []
    
   
   

    if request.user.is_authenticated:
        customer = request.user
  
        try:
            customer, created = Customer.objects.get_or_create(user = customer, name = customer.first_name + " " +  customer.last_name, email = customer.email)
            order = Order.objects.get(customer= customer, complete = False)
            orderid = order.orderid
            orderitems = order.orderitem_set.all()

            for items in orderitems:
                if items.product.product_name.remainingquantity != 0:
                    orderitemss.append(items)
            
                else:
                    pass


            shipping,created =  Shipping.objects.get(customer = customer, order = order )
    
         
   
        except:
            pass

        if request.method == "POST":
            shipping,created =  Shipping.objects.get_or_create(customer = customer,  order = order)
            shipping.address = request.POST.get("address")
            shipping.city = request.POST.get("city")
            shipping.contactnumber = request.POST.get("contactnumber")
            shipping.alternatenumber = request.POST.get("alternatenumber")
            shipping.save()
            return HttpResponseRedirect("/payment")
        
        try: 
            ship =  Shipping.objects.get(customer = customer,order = order)
        except: 
            pass
        try:
            allship = Shipping.objects.filter(customer=customer)
            allship = allship[:1]
        except:
            pass
        if orderid == None or order.get_cart_total == 0:
            return redirect(cart)
    else:
        CookieData = CookieCart(request)
        orderitems = CookieData['orderitems']
        order = CookieData['order']
        total = CookieData['total']
        ordertotal = order['get_cart_total']
        ordertotalwithshipping = order['get_cart_total_with_shipping']

        
        if not CookieData['order'] or ordertotalwithshipping == 0:
            return redirect(cart)

        try:
            shippingcookie = json.loads(request.COOKIES['shipping'])

            try:
                shiar = {
                        'total':shippingcookie['Shippingdata']['total'],
                        'fullname':shippingcookie['Shippingdata']['fullname'],
                        'email':shippingcookie['Shippingdata']['email'],
                        'address':shippingcookie['Shippingdata']['address'],
                        'city':shippingcookie['Shippingdata']['city'],
                        'contactnumber':shippingcookie['Shippingdata']['contactnumber'],
                        'alternatenumber':shippingcookie['Shippingdata']['alternatenumber'],
                }

            except:
                pass

            shiar.append(shiar)

        except:
            pass


        if request.method == "POST":
            return HttpResponseRedirect("/payment")


   

    if request.user.is_authenticated:
        context = {"orderitems":orderitemss,"order":order, "ship":ship, "alladdress":allship,"orderuniqueid":orderuniqueid}
    
    else:
        context = {"orderitems":orderitems,"order":order, 'ship':shiar, "alladdress":allship,"orderuniqueid":orderuniqueid}
    
    return render(request,"checkout.html",context)




def payment(request):
    
    orderitems = None
    order = None
    ship = None
    shiar = []
    special = []
    paymentmethod = []
    shippingcookie = None
    firstform = request.POST.get('form-1')
    secondform = request.POST.get("form-2")
    thirdform = request.POST.get('form-3')
    customer = None
    orderspecialinstruction = None
    orderpaymentmethod = None
    paymentmethod = request.POST.get("radio")
    
    if request.user.is_authenticated:
        customer = request.user
        customer, created = Customer.objects.get_or_create(user = customer, name = customer.first_name + " " +  customer.last_name, email = customer.email)
        try:
            order = Order.objects.get(customer = customer, complete = False)
            orderid = order.orderid
            orderitems = order.orderitem_set.all()
        except:
            pass

        try:
            orderpaymentmethod =  Order.objects.get(customer = customer,orderid = orderid)
        except:
            pass

        if request.method == "POST":
                if secondform == "form-2":
                    specialinstruction = request.POST.get("specialinstructions")
                    try:
                        orderspecialinstruction =  Order.objects.get(customer=customer,orderid = orderid)
                        orderspecialinstruction.specialinstructions = specialinstruction
                        orderspecialinstruction.save(update_fields = ["specialinstructions"])
                        return HttpResponseRedirect("/payment")
                    except:
                        pass
        if request.method == "POST":
            if firstform == "form-1":
                    shipping,created =  Shipping.objects.get_or_create(customer = customer, order = order)
                    shipping.address = request.POST.get("address")
                    shipping.city = request.POST.get("city")
                    shipping.contactnumber = request.POST.get("contactnumber")
                    shipping.alternatenumber = request.POST.get("alternatenumber")
                    shipping.save()

            if thirdform == "form-3":
                    orderpaymentmethod.paymentmethod = paymentmethod
                    orderpaymentmethod.status = "Order Placed"
                    orderpaymentmethod.save(update_fields = ["paymentmethod","status"])
                    return redirect(orderconfirmed)
         
        try: 
            ship =  Shipping.objects.get(customer = customer,order = order)

        except: 
            pass
        if orderid == None or order.get_cart_total == 0:
            return redirect(cart)
    
    else:
        CookieData = CookieCart(request)
        orderitems = CookieData['orderitems']
        order = CookieData['order']

        total = CookieData['total']
        ordertotal = order['get_cart_total']
        ordertotalwithshipping = order['get_cart_total_with_shipping']
        

        try:
            shippingcookie = json.loads(request.COOKIES['shipping'])
       

            try:
                shiar = {
                        'total':shippingcookie['Shippingdata']['total'],
                        'fullname':shippingcookie['Shippingdata']['fullname'],
                        'email':shippingcookie['Shippingdata']['email'],
                        'address':shippingcookie['Shippingdata']['address'],
                        'city':shippingcookie['Shippingdata']['city'],
                        'contactnumber':shippingcookie['Shippingdata']['contactnumber'],
                        'alternatenumber':shippingcookie['Shippingdata']['alternatenumber'],
                }

            except:
                pass

            shiar.append(shiar)
        except:
            pass

        try:
            specialcookie = json.loads(request.COOKIES['specialinstruct'])
            special = {
                'specialinstruction':specialcookie['specialinstruct']['instruction']
                }
        
        except:
            pass

        try:
            paymentmethod = json.loads(request.COOKIES['paymentmethod'])
            paymentmethod = {
                'paymentmethod':paymentmethod['paymentmethod']['paymentmethod']
            
            }
        
        except: 
            pass


        if request.method == "POST":
            if thirdform == "form-3":
                return redirect(orderconfirmed)
            

        
        if not CookieData['order'] or ordertotalwithshipping == 0:
            return redirect(cart)

  

        
    context = {"orderitems":orderitems,"order":order,"ship":ship, 'shipp':shiar, "orderpaymentmethod":orderpaymentmethod, "specialinstruction":special}
    return render(request,"payment.html",context)

def profile(request):
    total = 0
    if request.user.is_authenticated:
        customer = request.user
        orderitems = None
        order = None
        try:
            order = Order.objects.get(customer__user__email = customer, complete = False)
            orderitems = order.orderitem_set.all()
            total =  order.get_cart_items
   
        except:
            pass
    
    else:
        CookieData = CookieCart(request)
        orderitems = CookieData['orderitems']
        order = CookieData['order']
        total = CookieData['total']

       

    context = {"total":total}
    return render(request,"profile.html",context)


def ordertracking(request):

    total = 0
    orderitems = None
    order = None
    orderstatus = None
    orderid = request.GET.get("orderid")
    shipping = None
    orde = None

    try:
        orderstatus = Order.objects.get(orderid = orderid) 

        orderitems = orderstatus.orderitem_set.all()

        shipping = Shipping.objects.get(order = orderstatus)
        
    except:
        if orderid:
            messages.error(request, f"You Have Entered an Invalid Order ID, {orderid}")
        else:
            pass


   
    context = {"total":total, "orderstatus":orderstatus,"orderitems":orderitems,"shipping":shipping}

    return render(request, "ordertracking.html",context)
    



def orderconfirmed(request):

    total = 0
    customer = request.user
    orderitems = None
    order = None
    shiar = []
    orderid = None



    if request.user.is_authenticated:
        try:
            order = Order.objects.get(customer__user__email= customer, complete = False)
            orderitems = order.orderitem_set.all()
            order.ordertotal = order.get_cart_total_with_shipping
            for items in orderitems:
                if items.product.product_name.remainingquantity == 0:
                    prodname = items.product
                    orderitemproduct = OrderItem.objects.filter(order = order, product = prodname).delete()

            order.complete = True
            orderid = order.orderid
            order.save(update_fields = ['complete', 'ordertotal'])
         
            
  
        except:
            pass
        if orderid == None or order.get_cart_total == 0:
            return redirect(cart)

    
    else:
        try:

            shippingcookie = json.loads(request.COOKIES['shipping'])

            try:
                shiar = {
                        'total':shippingcookie['Shippingdata']['total'],
                        'fullname':shippingcookie['Shippingdata']['fullname'],
                        'email':shippingcookie['Shippingdata']['email'],
                        'address':shippingcookie['Shippingdata']['address'],
                        'city':shippingcookie['Shippingdata']['city'],
                        'contactnumber':shippingcookie['Shippingdata']['contactnumber'],
                        'alternatenumber':shippingcookie['Shippingdata']['alternatenumber'],
                }
                shiar.append(shiar)
            except:
                pass

            CookieData = CookieCart(request)
            orderitems = CookieData['orderitems']

            customer,created = Customer.objects.get_or_create(email = shiar['email'], name = shiar['fullname'] )

        
            order = Order.objects.get(customer = customer, complete = False)
            order.complete = True
            order.save(update_fields = ['complete'])
            orderid = order.orderid

        except:
            pass
        if not orderid:
            return redirect(cart)
        

           

   






 


        
        

    context = {"total":total,"order":order,"orderid":orderid}
    return render(request,"conformation.html",context)


def productdetails(request,productid):
    
    total = 0
    product = Product.objects.get(productid = productid)
    customerr = request.user
  
    quantity = request.POST.get('quantity')
    firstform = request.POST.get('form-1')

    orderItem = " "
    order = " "
    averagerate = []


    if request.user.is_authenticated:
        customer = request.user.email
        try:
            order = Order.objects.get(customer__user__email = customer, complete = False)
            orderItem = OrderItem.objects.get(order = order,product = product)
            total = order.get_cart_items
        except:
            pass
        if request.method == "POST":
            customer, created = Customer.objects.get_or_create(user = customerr, name = customerr.first_name + " " +  customerr.last_name, email = customerr.email)
            if firstform == "form-1":
                order, created = Order.objects.get_or_create(customer = customer, complete = False)
                orderItem, created = OrderItem.objects.get_or_create(order = order, product = product)
                orderItem.quantity = quantity
                orderItem.save()
                order = Order.objects.get(customer= customer,complete = False)
                orderItem = OrderItem.objects.get(order = order,product = product)
                total = order.get_cart_items
                
            else:
                pass
        
    else:
        CookieData = CookieCart(request)
        orderitems = CookieData['orderitems']
        order = CookieData['order']
        total = CookieData['total']

       




    products = Product.objects.filter(productid=productid)
    name = products[0].product_name
    ReviewsA = ""
 


    test = Reviews.objects.filter(ProductName = name)
    objcount = 0
    randomobj = []


    randomselect = Product.objects.exclude(productid=productid)
    for obj in randomselect:
        randomobj.append(obj)
    objcount = len(randomobj)

    
    rand = random.sample(randomobj,objcount)
    rand = rand[:4]

 
    arr = []
    z = 0
    z2 = 0
    rating2 = 0
    rating = 0
    i = 0
    num2 = 0
    a = 0


    used = 0
    for num in test:
       arr.append((num.Email).upper())
       z += 1
    num = len(arr)

    reviews = ''
    
    form1 = ReviewForm()
    rate1 = request.POST.get('rate1')
    rate2 = request.POST.get('rate2')
    rate3 = request.POST.get('rate3')
    rate4 = request.POST.get('rate4')
    rate5 = request.POST.get('rate5')

    z = 0

    Email = ""
    email = ""

    product = Product.objects.get(productid = productid)
    n = product.product_name


    bestsellers = BestSellers.objects.all()
    allowedquantity = int((products[0].allowedquantity))
    productview = product.views + 1
    product.views = productview


    product.save(update_fields=['views'])
   
    if request.method == "POST":
        if firstform != "form-1":
            reviews =  Reviews.objects.filter(ProductName = name)
            form = ReviewForm(request.POST,request.FILES)
            email = request.POST.get('Email')
            try:
                Email = request.POST.get('Email').upper()
                for rate in reviews:
                    rating = (rating + reviews[i].Rating)
                    i = i + 1
                rating = math.ceil(rating/i)
            except:
                pass

            if form.is_valid():
                instance = form.save(commit = False)
                instance.ProductName = products[0].product_name
                for check in arr:
                    if Email == str(arr[z]):
                        used = 1
                    z += 1
                if rate1 == "1":
                    instance.Rating = 1
                elif rate2 == "2":
                    instance.Rating = 2
                elif rate3 == "3":
                    instance.Rating = 3
                elif rate4 == "4":
                    instance.Rating = 4
                elif rate5 == "5":
                    instance.Rating = 5
                
                if used == 1:
                    pass
                else:
                    form.save()
                    messages.success(request,f"Your Rating has been successfully submitted")  
                
    else:
        form = ReviewForm()
    test2 = Reviews.objects.filter(ProductName = name).order_by("-Date")
    
    try:
    
        for num in test2:
            rating2 = rating2 + test2[num2].Rating
            num2 +=1
        rating2 = math.ceil(rating2/num2)

    except:
        pass

    
    product.rate = rating2
  
    product.save(update_fields = ['rate'])
    
    if request.user.is_authenticated:
        try:
            order = Order.objects.get(customer__user__email = customer, complete = False)
            orderItem = OrderItem.objects.get(order = order,product = product)
            total = order.get_cart_items
        except:
            pass
    else:
        pass
   

    context = {"total":total,"order":orderItem,"product":products,"allowed":allowedquantity,"form1":form1,"rate":rating2,"used":used,"Email":email,"totalreview":num2,"reviews":test2,"name":name,"bestsellers":bestsellers,"randomproducts":rand}
    return render(request, "productdescription.html", context)



def CategoryName(request,category):
    total = 0
    if request.user.is_authenticated:
        customer = request.user
        orderitems = None
        order = None
        try:
            order = Order.objects.get(customer__user__email = customer, complete = False)
            orderitems = order.orderitem_set.all()
            total = order.get_cart_items
   
        except:
            pass
    else:
        CookieData = CookieCart(request)
        orderitems = CookieData['orderitems']
        order = CookieData['order']
        total = CookieData['total']

       

    products =  Product.objects.filter(product_name__category = category)
    category = category
    length = len(products)
    boxcontent = "Sort"

    if request.method == "GET":
        try:
            answer = request.GET['query']
        except:
            pass
        
    try:
        if answer == "SortByPricedesc":
            products = Product.objects.filter(product_name__category = category).order_by('-price')
            boxcontent = "Sort By Price: High To Low"
        elif answer == "SortByPrice":
            products = Product.objects.filter(product_name__category = category).order_by('price')
            boxcontent = "Sort By Price: Low To High"
        elif answer == "SortByBrand":
            products = Product.objects.filter(product_name__category = category).order_by('product_name')
            boxcontent = "Sort By Brand"
        elif answer == "SortByDateAdded":
            products = Product.objects.filter(product_name__category = category).order_by('-dateadded')
            boxcontent = "Sort By Date Added"
    except:
        pass

    context ={"total": total, "product":products,"number":length,"boxcontent":boxcontent,"category":category}
    return render(request, "category.html",context)


def UpdateItem(request):



    data = json.loads(request.body)
    productid = data['productid']
    action = data['action']
    product = Product.objects.get(productid = productid)

    customer = request.user
    customer, created = Customer.objects.get_or_create(user = customer, name = customer.first_name + " " +  customer.last_name, email = customer.email)
    order, created = Order.objects.get_or_create(customer= customer, complete = False)

  
    orderItem, created = OrderItem.objects.get_or_create(order = order, product = product)

    maximumfetch = OrderItem.objects.get(order = order, product = product)
    maxquantity = int(maximumfetch.product.allowedquantity)
    quantity = int(orderItem.quantity)
      
    if orderItem.quantity == 0:
        if action == "add":
            orderItem.quantity = orderItem.quantity + 1
            messages.success(request, f"{product.product_name} is successfully added to your cart.")

        elif action == "addcart": 
            orderItem.quantity = orderItem.quantity + 1
        
        elif action == "remove":
            orderItem.quantity = orderItem.quantity - 1

    elif orderItem.quantity !=0:
        if action == "add-update":
            if quantity < maxquantity:
                orderItem.quantity = orderItem.quantity + 1
            else:
                messages.error(request, "Maxmium Allowed Quantity Reached" )
        elif action == "remove-update":
            orderItem.quantity = orderItem.quantity - 1
        elif action == "add":
            messages.error(request, f"This Product is already in your cart")
    else:
        pass



    orderItem.save()
    if orderItem.quantity<=0:
            orderItem.delete() 
        


    return JsonResponse('Item Was Added',safe=False)


def shippinginfo(request):


    data = json.loads(request.body)

    if request.method == "POST":
        name = data['form']['fullname']
        address = data['form']['address']
        city = data['form']['city']
        contactnumber = data['form']['contactnumber']
        alternatenumber = data['form']['alternatenumber']
        total = data['form']['total']
        email = data['form']['email'].lower()
    
        CookieData = CookieCart(request)
        orderitems = CookieData['orderitems']
        orderitemswithout = []

    
        for items in orderitems:
            if items['remainingquantity'] != 0:
                orderitemswithout.append(items)
        print(orderitemswithout)
        


        customer, created = Customer.objects.get_or_create(email = email)
        customer.name =  name
        customer.save()
        order,created = Order.objects.get_or_create(customer = customer, complete = False, ordertotal = total)
        print(order.orderid)
        shipping, created = Shipping.objects.get_or_create(customer = customer, order = order, address = address, city = city, contactnumber = contactnumber, alternatenumber = alternatenumber )
        shipping.save(0)
        for item in orderitemswithout: 
            product = Product.objects.get(productid = item['product']['productid'])
            orderitems, created= OrderItem.objects.get_or_create(order = order, product = product, quantity = item['quantity'])
        order.status = "Order Placed"
        order.specialinstructions = data['instruction']['instruction']
        order.paymentmethod = data['payment']['paymentmethod']
        order.save(update_fields = ["status","paymentmethod","specialinstructions"])


        
    else:
        pass 



    return JsonResponse("ShippingInfo",safe = False)
