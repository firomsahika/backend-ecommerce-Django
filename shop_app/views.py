from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from django.conf import settings
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Product,Cart, CartItem,ChapaTransaction
from decimal import Decimal
from django.apps import apps
from .serializers import RegistrationSerializer  ,UserSerializer,ProductSerializer,CartSerializer,DetailedProductSerializer,SimpleCartSerializer,CartItemSerializer
from django.views.decorators.csrf import csrf_exempt
from .api import ChapaAPI
from django.http import JsonResponse
import json
from django.conf import settings
from django.http import JsonResponse
from .services.scraper import scrape_product_data
from langchain_community.llms import OpenAI
from urllib.parse import urlparse



BASE_URL = settings.REACT_BASE_URL

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
    print(f"Serialized data: {serializer.data}")
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


def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False
    

@api_view(['GET'])
def get_scraped_products(request):
    url = request.GET.get("url", "https://shoppit-jqdk.onrender.com/")
    
    if not is_valid_url(url):
        return JsonResponse({"error": "Invalid URL provided."}, status=400)
    
    try:
        scraped_data = scrape_product_data(url)
        return JsonResponse({"products": scraped_data})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
    
@csrf_exempt
def chat_response(request):
    if request.method == "POST":
        user_message = request.POST.get('message')
        product_url = request.POST.get('url', "https://shoppit-jqdk.onrender.com/")

        products = scrape_product_data(product_url)

        product_info = "\n".join([f"Product: {p['name']}, Price: {p['price']}, ram: {p['ram']}" for p in products])

        prompt = f"{user_message}\n Here are product detail:\n {product_info}"

        llm= OpenAI(temperature=0)

        bot_response = llm(prompt)

        return JsonResponse({"bot_response": bot_response})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)