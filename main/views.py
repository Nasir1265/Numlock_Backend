from django.shortcuts import render
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from main.serializers import Product_Serializer,ProductImg_Serializer,Register_Serializer,Login_Serializer,Book_Service_Serializer,Contact_form_Serializer
from .models import Products,Order,Payment
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework import status,generics
from django.http import JsonResponse
# Create your views here.
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.utils import timezone
import hmac
import hashlib
import logging

# views.py

def ping(request):
    return JsonResponse({"status": "alive"})
    
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





logger = logging.getLogger(__name__)

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

@api_view(['POST'])
def create_order(request):
    try:
        product_id = request.data.get('product_id')
        # user_email = request.data.get('user_email')
        product = Products.objects.get(product_id=product_id)
        receipt_str = f"order_rcptid_{product_id}"[:40]
        # Create Razorpay order
        order_data = {
            'amount': int(product.price * 100),  # Amount in paise
            'currency': 'INR',
            'receipt': receipt_str,
        }
        razorpay_order = client.order.create(data=order_data)
        
        # Save order in database
        order = Order.objects.create(
            product=product,
            # user_email=user_email,
            amount=product.price,
            razorpay_order_id=razorpay_order['id'],
        )
        
        return JsonResponse({
            'order_id': razorpay_order['id'],
            'amount': order_data['amount'],
            'currency': order_data['currency'],
            'key': settings.RAZORPAY_KEY_ID,
        })
    except Products.DoesNotExist:
        logger.error(f"Product not found: {product_id}")
        return JsonResponse({'error': 'Product not found'}, status=404)
    except Exception as e:
        logger.error(f"Error creating order: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['POST'])
@csrf_exempt
def verify_payment(request):
    try:
        razorpay_payment_id = request.data.get('razorpay_payment_id')
        razorpay_order_id = request.data.get('razorpay_order_id')
        razorpay_signature = request.data.get('razorpay_signature')
        
        # Verify signature
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
        }
        generated_signature = hmac.new(
            settings.RAZORPAY_KEY_SECRET.encode(),
            f"{razorpay_order_id}|{razorpay_payment_id}".encode(),
            hashlib.sha256
        ).hexdigest()
        
        if generated_signature != razorpay_signature:
            logger.error(f"Invalid signature for order {razorpay_order_id}")
            return JsonResponse({'error': 'Invalid signature'}, status=400)
        
        # Update order and save payment
        order = Order.objects.get(razorpay_order_id=razorpay_order_id)
        order.status = 'paid'
        order.save()
        
        Payment.objects.create(
            order=order,
            razorpay_payment_id=razorpay_payment_id,
            razorpay_signature=razorpay_signature,
            status='success'
        )
        
        return JsonResponse({'status': 'Payment successful'})
    except Order.DoesNotExist:
        logger.error(f"Order not found: {razorpay_order_id}")
        return JsonResponse({'error': 'Order not found'}, status=404)
    except Exception as e:
        logger.error(f"Error verifying payment: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)