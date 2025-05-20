from django.shortcuts import render
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from main.serializers import Product_Serializer,ProductImg_Serializer,Register_Serializer,Login_Serializer,Book_Service_Serializer,Contact_form_Serializer
from .models import Products
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework import status,generics
# Create your views here.

class Register(CreateAPIView):
    queryset=User.objects.all()
    serializer_class=Register_Serializer
 

class Login(APIView):
    permission_classes = [AllowAny]
    def post(self,request): 
        serializers=Login_Serializer(data=request.data)
        if serializers.is_valid():
            username=serializers.validated_data['username']
            password=serializers.validated_data['password']

            if not User.objects.filter(username=username).exists():
                return Response({
                    "errors":"username does not exist."
                },status=400)

            user=authenticate(username=username,
                              password=password)
            if user is None:
                return Response({
                    "errors":"Incorrect Password..."
                },status=400)
            token,created=Token.objects.get_or_create(user=user)
            return Response({
                    "Message":"Login Successfully..",
                    "Token":token.key,

                },status=200)
        else:
            return Response({
                    "errors":serializers.errors,
                    },status=400)


class Product_List(ListAPIView):
    queryset=Products.objects.all()
    serializer_class=Product_Serializer

    def list(self, request, *args, **kwargs):
        response= super().list(request, *args, **kwargs)
        custom_data={
            "count":self.get_queryset().count(),
            "data":response.data
        }
        return Response(custom_data)

class Best_Seller(ListAPIView):
    queryset=Products.objects.filter(bestseller=True)
    serializer_class=Product_Serializer

    def list(self, request, *args, **kwargs):
        respose = super().list(request, *args, **kwargs)
        custom_data={
            "count":self.get_queryset().count(),
            "data":respose.data
        }
        return Response(custom_data)


class Latest_Item(ListAPIView):
    queryset=Products.objects.filter(latest_items=True)
    serializer_class=Product_Serializer


class ProductCreateView(generics.CreateAPIView):
    queryset = Products.objects.all()
    serializer_class = Product_Serializer
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Brand_service(APIView):
    def post(self, request, *args, **kwargs):
        serializer = Book_Service_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Booking successful"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
class Contact_form(APIView):
    def post(self, request, *args, **kwargs):
        serializer = Contact_form_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Form successful Submit"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
