from rest_framework import serializers
from .models import Product,Cart,CartItem,ChapaTransaction
from django.contrib.auth import get_user_model
from decimal import Decimal

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','name','slug','ram','image','description','category','price']


class DetailedProductSerializer(serializers.ModelSerializer):
    similar_products = serializers.SerializerMethodField()

    def get_similar_products(self, product:Product):
        products =  Product.objects.filter(category=product.category).exclude(id=product.id)
        serializer = ProductSerializer(products, many=True)
        return serializer.data

    class Meta:
        model = Product
        fields = ['id','name','slug','image','price','description', 'similar_products'  ]
        

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    total = serializers.SerializerMethodField()
    
    class Meta:
        model = CartItem
        fields = ['id','quantity','product', 'total']

    def get_total(self, cartitem):
        price = cartitem.product.price * cartitem.quantity
        return price


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(read_only=True, many=True)
    num_of_items = serializers.SerializerMethodField()
    sum_total = serializers.SerializerMethodField()
    class Meta:
        model = Cart
        fields = ['id','cart_code','user','items','sum_total','num_of_items', 'paid']

    def get_sum_total(self, cart):
        items = cart.items.all()
        total = sum([item.product.price * item.quantity for item in items])
        return total
    
    def get_num_of_items(self, cart):
        items = cart.items.all()
        total = sum([item.quantity for item in items])
        return total


class SimpleCartSerializer(serializers.ModelSerializer):
    num_of_items = serializers.SerializerMethodField()

    def get_num_of_items(self, cart:Cart):
        num_of_items = sum([item.quantity for item in cart.items.all()])
        return num_of_items
    
    class Meta:
        model = Cart
        fields = ['id', 'cart_code', 'num_of_items']



      
class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)  # Add confirm_password field

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'phone', 'first_name', 'last_name', 'password', 'confirm_password']  # Remove the comma here

    def validate(self, data):  
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
       
        validated_data.pop('confirm_password')

        # Create a new user instance
        user = get_user_model()(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone=validated_data['phone'],
            email=validated_data['email'],
        )

        # Set the user's password securely
        user.set_password(validated_data['password'])
        user.save()

        return user


class NewCartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    order_id = serializers.SerializerMethodField()
    order_date = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity','order_id', 'order_date']

    def get_order_id(self, cartitem):
        order_id = cartitem.cart.cart_code
        return order_id

    def get_order_date(self, cartitem):
        order_date = cartitem.cart.modified_at
        return order_date




class UserSerializer(serializers.ModelSerializer):
    order_items = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()  # This retrieves the user model
        fields = ['id', 'username', 'email', 'phone', 'first_name', 'last_name','order_items'] 

    def get_order_items(self, user):
        
        cartitems = CartItem.objects.filter(cart__user=user, )[:10]
        serializer = NewCartItemSerializer(cartitems, many=True)
        return serializer.data

    