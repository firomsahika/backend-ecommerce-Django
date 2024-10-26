from django.urls import path
from . import views

urlpatterns =[
    path("products/", views.products, name='products'),
    path("product_detail/<slug:slug>", views.product_detail, name="product_detail"),
    path("add_item/", views.add_item, name="add_item"),
    path("product_in_cart/", views.product_in_cart, name="product_in_cart"),
    path("get_cart_stat", views.get_cart_stat, name="get_cart_stat"),
    path("get_cart", views.get_cart, name="get_cart"),
    path("update_quantity/", views.update_quantity, name="update_quantity"),
    path("delete_item", views.delete_item, name="delete_item"),
    path("product_category/<str:category>/", views.product_category, name="product_category"),
    path("product_ram/<str:ram>/", views.product_ram, name="product_ram"),
    path("get_user_info", views.get_user_info, name="get_user_info"),
    path("search_product/<str:name>", views.search_product, name="search_product"),
    path("register/", views.register, name="register"),
    path('chapa_webhook/', views.chapa_webhook, name='chapa_webhook'),
   
]
