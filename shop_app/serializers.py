from rest_framework import serializers
from .models import Product,Cart,CartItem


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','name','slug','image','description','category','price']


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

    
    

