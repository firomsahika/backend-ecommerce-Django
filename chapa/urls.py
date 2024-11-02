from django.urls import path
from . import views



urlpatterns = [
    path('', views.chapa_webhook),
    path('initialize_payment/', views.initialize_payment, name="initialize_payment")

]
