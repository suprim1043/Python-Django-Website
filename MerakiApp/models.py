from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid
from PIL import Image

import datetime
from uuid import uuid4
# Create your models here.




pagechoice = (
  ("1","1"),
  ("2","2"),
  ("3","3"),

)


allowedquantity = (

  ("1","1"),
  ("2","2"),
  ("3","3"),
  ("4","4"),
  ("5","5"),
  ("6","6"),
  ("7","7"),
  ("8","8"),
  ("9","9"),
  ("10","10"),
)

paymentchoice = (
    ("COD","COD"),
    ("ESEWA","ESEWA"),
    ("BANK TRANSFER","BANKTRANSFER"),
    ("FONEPAY","FONEPAY"),
)

orderstatus = (
    ("Order Placed", "Order Placed"),
    ("Acknowledged", "Acknowledged"),
    ("Out For Delivery", "Out For Delivery"),
    ("Delivered", "Delivered")




)



class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class myuser(AbstractUser):
    userid = models.CharField(default=uuid.uuid4, primary_key = True, unique = True,  editable = False, max_length = 200)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    username = None
    email = models.EmailField(_('email address'), unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        for field_name in ['email' ]:
            val = getattr(self, field_name, False)
            if val:
                setattr(self, field_name, val.lower())
        for field_name in ['first_name','last_name' ]:
            val = getattr(self, field_name, False)
            if val:
                setattr(self, field_name, val.title())
        super(myuser, self).save(*args, **kwargs)

    def __str__(self):
        return (self.email) 


class Customer(models.Model):
    user = models.OneToOneField(myuser, on_delete = models.CASCADE, null = True, blank = True)
    name = models.CharField(max_length = 200, null = True, blank = True)
    email = models.EmailField(null = True, blank = True, unique = True)

    def __str__(self):
        return (self.name) 


class Category(models.Model):
    category = models.CharField(max_length=200, null = False, primary_key = True,default = "")
    image = models.ImageField(blank = True, null = True)
    def __str__(self):
        return(self.category)


class Stock(models.Model):
    product_name = models.CharField(max_length =200, blank = True, null = True, unique = True)
    quantity = models.IntegerField(default = 0)
    category = models.ForeignKey(Category, on_delete = models.SET_NULL, null = True)
    remainingquantity = models.IntegerField(default = 0)
    size = models.CharField(max_length = 200, blank = True, null = True)
    date = models.DateTimeField(auto_now_add = True)
    uploadedby = models.ForeignKey(myuser, on_delete = models.SET_NULL, null = True)

    class Meta:
         verbose_name_plural = "Stock"
    def __str__(self):
        return str(self.product_name)
    def save(self, *args, **kwargs):
        if not self.id:
            self.remainingquantity = self.quantity
        super(Stock, self).save(*args, **kwargs)

class Reviews(models.Model):
    ProductName = models.ForeignKey(Stock,on_delete=models.CASCADE)
    Email = models.EmailField(blank = False,null = True)
    Name = models.CharField(max_length=200, blank = False,default="0")
    Date = models.DateTimeField(auto_now_add = True,null = True)
    Text = models.TextField(blank = False,default="",max_length=400)
    Image1 = models.ImageField(blank = True,null = True)
    Image2 = models.ImageField(blank = True,null = True)
    Rating = models.IntegerField(blank = False,null = True, default = 0)

    class Meta:
         verbose_name_plural = "Reviews"

    def __str__(self):
        return (str(self.ProductName))


class Product(models.Model):
    product_name = models.OneToOneField(Stock,on_delete = models.CASCADE,blank = True, null = True,unique=True)
    name = models.CharField(max_length = 200, null = True, blank = True,editable=False)
    price = models.FloatField()
    dateadded = models.DateTimeField(auto_now_add = True, blank = True, null = True)
    firstimage = models.ImageField(blank = True, null = True)
    second = models.ImageField(blank = True, null = True)
    thirdimage = models.ImageField(blank = True, null = True)
    allowedquantity = models.CharField(max_length = 200,blank = True, choices = allowedquantity)
    productid = models.UUIDField(default=uuid.uuid4, primary_key = True, unique = True,  editable = False)
    description = models.TextField(blank = True, null = True, max_length = 1000)
    rate = models.IntegerField(blank = True, null = True, default = 0)
    views = models.IntegerField(blank = False, null = False, default = 0)


    def __str__(self):
        return str((self.product_name))

def create_id():
    now = datetime.datetime.now()
    return str(now.year)+str(now.month)+str(now.day)+str(uuid4())[:4]
    

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete = models.CASCADE, blank = True, null = True)
    date_ordered = models.DateTimeField(auto_now_add = True)
    complete = models.BooleanField(default = False, null = True, blank = False)
    orderid = models.CharField(max_length = 200, blank = True, default = create_id, unique=True)
    status = models.CharField(max_length = 200, blank = True, null = True, choices = orderstatus)
    ordertotal = models.DecimalField(blank = True, null = True, max_digits = 10, decimal_places = 2)
    paymentstatus = models.BooleanField(default = False, null = True, blank = False)
    paymentmethod = models.CharField( max_length = 50, blank = True, null = True,  choices = paymentchoice)
    specialinstructions = models.CharField(max_length = 200, blank = True, null = True)
    expectedarrival = models.DateField(null = True)
    
    def __str__(self):
        return str(self.orderid + " ,  " + self.customer.name) 
    
    @property 
    def get_cart_items(self):
         orderitems = self.orderitem_set.all()
         total = sum([item.quantity for item in orderitems])
         return total
    @property 
    def get_cart_total(self):
         orderitems = self.orderitem_set.all()
         total = sum([item.get_total for item in orderitems])
         totalwithshipping = total + 100
         return total
         return totalwithshipping
    @property 
    def get_cart_total_with_shipping(self):
         orderitems = self.orderitem_set.all()
         total = sum([item.get_total for item in orderitems])
         totalwithshipping = total + 100
         return totalwithshipping
 

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete = models.SET_NULL, blank = True, null = True)
    order = models.ForeignKey(Order,on_delete = models.CASCADE, blank = True, null = True)
    quantity = models.IntegerField(default = 0, null = True, blank = True)
    date_added = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return str((self.product)) 
    @property
    def get_total(self):
        total = 0
        if self.product.product_name.remainingquantity != 0:
            total = (self.product.price * self.quantity)
            
        else:
            pass
        return total

 



class Shipping(models.Model):
    customer = models.ForeignKey(Customer, on_delete = models.CASCADE, blank = True, null = True)
    order = models.ForeignKey(Order,on_delete = models.CASCADE, blank = True, null = True)
    address = models.CharField(max_length =200,  blank = True, null = True)
    city = models.CharField(max_length =200,  blank = True, null = True)
    contactnumber = models.IntegerField(default = None, blank = True, null = True)
    alternatenumber = models.IntegerField(default = None, blank = True, null = True)
    date_added = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return str(self.customer) 


class Homepage_Slider(models.Model):
   
    Page = models.CharField(choices = pagechoice, max_length = 3, blank = False, default = 1, primary_key = True)
    ImageFirst = models.ImageField(blank=False)
    ImageSecond = models.ImageField(blank=False, default = 1)
    Title  = models.CharField(max_length = 50, blank = False)
    Description = models.TextField(max_length = 30, blank = False)
    LinkName = models.CharField(blank = False, default = "View Details", max_length=50)
    Link_Content = models.CharField(blank = False, max_length = 300, default = 1)

    class Meta:
         verbose_name_plural = "Homepage Slider"

    def __str__(self):
        return str(self.Page)



class BestSellers(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE, null = True, blank = True)
    
    def __str__(self):
        return str(self.product)
         
    class Meta:
         verbose_name_plural = "Best Seller"




class ContactModel(models.Model):
    Userid = models.CharField(max_length = 200, blank = True)
    FullName =  models.CharField(max_length = 200, null = False, blank = False)
    Email = models.EmailField(blank = False, null = False)
    Query = models.TextField(blank = False, null = False)
    DateAdded = models.DateTimeField(auto_now_add = True, null = True)
    
    class Meta:
         verbose_name_plural = "Contact"

    def __str__(self):
        return (str(self.FullName) + " " + str(self.DateAdded.strftime("%Y-%m-%d %H:%M:%S")) + "  " + str(self.Query[0:10]))




