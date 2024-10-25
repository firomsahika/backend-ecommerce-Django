from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Product,Cart, CartItem
from decimal import Decimal

from .serializers import RegistrationSerializer,UserSerializer,ProductSerializer,CartSerializer,DetailedProductSerializer,SimpleCartSerializer,CartItemSerializer
import requests
import hashlib
import json
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt




BASE_URL = "http://localhost:5173/"
TELEBIRR_BASE_URL = "https://api.telebirr.com/v1/payments"

@api_view(['GET'])
def products(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def product_detail(request, slug):
    product = Product.objects.get(slug=slug)
    serializer = DetailedProductSerializer(product)
    return Response(serializer.data)

@api_view(['POST'])
def add_item(request):
    try:
        cart_code = request.data.get('cart_code') 
        product_id = request.data.get('product_id') 

        cart, created = Cart.objects.get_or_create(cart_code=cart_code) 
        product = Product.objects.get(id=product_id)

        cartitem, created = CartItem.objects.get_or_create(cart=cart, product=product)
        cartitem.quantity = 1
        cartitem.save()

        serializer = CartItemSerializer(cartitem)
        return Response({"data":serializer.data, "message":"cart item created succesfully!"}, status=201)
    except Exception as e:
        return Response({"error":str(e)}, status=400)

@api_view(['GET'])
def product_in_cart(request):
    cart_code = request.query_params.get("cart_code")
    product_id  = request.query_params.get("product_id")

    cart = Cart.objects.get(cart_code=cart_code)
    product = Product.objects.get(id=product_id)

    product_exists_in_cart = CartItem.objects.filter(cart=cart, product=product).exists()
    
    return Response({'product_in_cart': product_exists_in_cart })

@api_view(['GET'])
def get_cart_stat(request):
    cart_code = request.query_params.get("cart_code")
    cart = Cart.objects.get(cart_code=cart_code)
    serializer = SimpleCartSerializer(cart)
    return Response(serializer.data)

@api_view(['GET'])
def get_cart(request):
    cart_code = request.query_params.get("cart_code")
    cart = Cart.objects.get(cart_code=cart_code, paid=False)
    serializer = CartSerializer(cart)
    return Response(serializer.data)

@api_view(['PATCH'])
def update_quantity(request):
    try:
        cartitem_id = request.data.get("item_id")
        quantity = request.data.get("quantity")
        quantity = int(quantity)
        cartitem = CartItem.objects.get(id=cartitem_id)
        cartitem.quantity = quantity
        cartitem.save()
        serializer = CartItemSerializer(cartitem)

        return Response({"data":serializer.data, 'message':'carrt updated successfully!'})
    except Exception as e:
        return Response({"error":str(e)}, status=400)


@api_view(['POST'])
def delete_item(request):
    try:
        cartitem_id = request.data.get("item_id")
        cartitem = CartItem.objects.get(id=cartitem_id)

        cartitem.delete()
        return Response({"message": " Item deleted succesfully!"}, status=200)
    except Exception as e:
        return Response({"err": str(e)}, status=400)

@api_view(['GET'])
def product_category(request, category):
    product = Product.objects.filter(category=category)
    serializer = ProductSerializer(product, many=True)

    return Response(serializer.data)

@api_view(['GET'])
def product_ram(request, ram):
    product = Product.objects.filter(ram=ram)
    serializer = ProductSerializer(product, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)


@api_view(['GET'])
def search_product(request, name):
    product = Product.objects.filter(name__icontains=name)  # Partial match
    serializer = ProductSerializer(product, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def register(request):
    serializer = RegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


# payment integration views

def generate_nonce():
    import uuid
    return str(uuid.uuid4())



@permission_classes([IsAuthenticated])
@csrf_exempt  
@api_view('[POST]')
def apply_fabric_token():
    BASE_URL = settings.BASE_URL
    fabric_app_id = settings.FABRIC_APP_ID
    app_secret = settings.APP_SECRET

    headers = {
        "Content-Type": "application/json",
        "X-APP-Key": fabric_app_id
    }
    payload = {
        "appSecret": app_secret
    }
    response = requests.post(f"{BASE_URL}/payment/v1/token", headers=headers, json=payload, verify=False)
    
    return response.json()

@csrf_exempt
def create_order(request):
    if request.method == "POST":
        
        title = "Payment request"

        cart_code = request.data.get('cart_code')
        cart = Cart.objects.get(cart_code=cart_code)
        user = request.user

        amount = sum([item.quantity * item.prouct.price for item in cart.items.all()])
        tax = Decimal("4.00")
        total_amount = amount + tax
        currency = "ETB"
        redirect_url = f"{BASE_URL}/payment-status"

        # Get the fabric token
        token_result = apply_fabric_token()
        fabric_token = token_result.get("token")

        # Create order
        order_result = request_create_order(fabric_token, title, total_amount)
        
        return JsonResponse(order_result)

def request_create_order(fabric_token, title, total_amount):
    BASE_URL = settings.BASE_URL
    fabric_app_id = settings.FABRIC_APP_ID
    merchant_app_id = settings.MERCHANT_APP_ID
    merchant_code = settings.MERCHANT_CODE
    notify_path = settings.NOTIFY_PATH

    headers = {
        "Content-Type": "application/json",
        "X-APP-Key": fabric_app_id,
        "Authorization": fabric_token
    }
    payload = create_request_object(title, total_amount, merchant_app_id, merchant_code, notify_path)
    response = requests.post(f"{BASE_URL}/payment/v1/merchant/preOrder", headers=headers, json=payload, verify=False)
    
    return response.json()

def create_request_object(title, total_amount, merchant_app_id, merchant_code, notify_path):
    # Construct your payload here based on the TeleBirr API requirements
    return {
        "title": title,
        "amount": total_amount,
        "merchantAppId": merchant_app_id,
        "merchantCode": merchant_code,
        "notifyPath": notify_path,
        "trans_currency": "ETB",
        # Add other required fields...
    }