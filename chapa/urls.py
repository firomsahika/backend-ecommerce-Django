from django.urls import path
from . import views



urlpatterns = [
    path('initialize_payment/', views.initialize_payment, name="initialize_payment"),
    path('api/chapa_webhook/', views.chapa_webhook, name='chapa_webhook'),

]
