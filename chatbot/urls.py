from django.urls import path
from . import views

urlpatterns = [
    path('api/chatbot/', views.chat, name="chat")
]