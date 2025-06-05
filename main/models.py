from django.db import models
import uuid
from cloudinary.models import CloudinaryField
from django.utils import timezone
# Create your models here.

# class Size(models.Model):
#     name=models.CharField(max_length=10,unique=True)
  
#     def __str__(self): 
#         return self.name
    
class Products(models.Model):
    CHOICE_CATEGORY=[("DELL","DELL"),
            ("MAC","MAC"),
            ("HP","HP")]
    # CHOICE_SUBCATEGORY=[("Topwear","Topwear"),
    #         ("Bottomwear","Bottomwear"),
    #         ("Winterwear","Winterwear")]
    product_id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False,unique=True)
    name =models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()
    category = models.CharField(max_length=100,choices=CHOICE_CATEGORY)
    # subCategory = models.CharField(max_length=100,choices=CHOICE_SUBCATEGORY)
    # sizes =models.ManyToManyField(Size,related_name='products')
    date = models.DateTimeField(auto_now_add=True)
    bestseller = models.BooleanField(default=False)
    latest_items = models.BooleanField(default=False) 
    
    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name="images")
    image = CloudinaryField('file', resource_type='auto', folder='products/')
    def __str__(self):
        return f"Image for {self.product.name}"



class Book_Service(models.Model):
    name=models.CharField(max_length=100)
    phone=models.CharField(max_length=20)
    email=models.EmailField()
    device_name=models.CharField(max_length=100)
    brand_name=models.CharField(max_length=100)
    device_issue=models.TextField()

    def __str__(self):
        return f"{self.name} - {self.device_name}"


class Contact_form(models.Model):
    full_name = models.CharField(max_length=1000)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return f"{self.full_name} - {self.subject}"


class Order(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    user_email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    razorpay_order_id = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, default='created')  # created, paid, failed

    def __str__(self):
        return f"Order {self.razorpay_order_id}"
 
class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    razorpay_payment_id = models.CharField(max_length=100, unique=True)
    razorpay_signature = models.CharField(max_length=255)
    status = models.CharField(max_length=20)  # success, failed
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Payment {self.razorpay_payment_id}"