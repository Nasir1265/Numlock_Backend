from rest_framework import serializers
from .models import Products,ProductImage,Book_Service,Contact_form
from django.contrib.auth.models import User



class Book_Service_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Book_Service
        fields = "__all__"

class Contact_form_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Contact_form
        fields = "__all__"


class Register_Serializer(serializers.Serializer):
    username=serializers.CharField()
    email=serializers.EmailField()
    password=serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
    def validate_username(self,value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("username already exists...")
        return value
    
    def validate_email(self,value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already Exists..")
        return value


class Login_Serializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()
 
 
class ProductImg_Serializer(serializers.ModelSerializer):
    class Meta:
        model=ProductImage
        fields=['image']

# class Size_Serializer(serializers.ModelSerializer):
#     class Meta: 
#         model=Size
#         fields=['id','name']

class Product_Serializer(serializers.ModelSerializer):
    image=serializers.ListField(child=serializers.ImageField(),write_only=True)
    # sizes = serializers.ListField(child=serializers.CharField(), write_only=True) 
    class Meta:
        model=Products
        fields=["product_id","name","description","price","category","date","bestseller","latest_items","image"]
    
    def create(self, validated_data):
        image=validated_data.pop('image',[])
        # sizes=validated_data.pop("sizes",[])

        product = Products.objects.create(**validated_data)
        
        # # ✅ Handle size saving and ManyToMany relation
        # for size_name in sizes:
        #     size_obj, created = Size.objects.get_or_create(name=size_name)# Get or create Size objects
        #     print(size_name)  
        #     product.sizes.add(size_obj)  # ✅ Add the size to the product

        for img in image:
            ProductImage.objects.create(product=product,image=img)
        return product

    
    def to_representation(self, instance):
        representation= super().to_representation(instance)
        representation['images']=[img.image.url for img in instance.images.all()]
        # representation["size"]=Size_Serializer(instance.sizes.all(),many=True).data
        return representation