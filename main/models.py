from django.db import models
import uuid

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
    image = models.ImageField(upload_to="products")

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