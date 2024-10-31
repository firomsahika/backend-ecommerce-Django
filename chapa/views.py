from django.shortcuts import render
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import ChapaTransaction
from django.contrib.auth.decorators import login_required
from django.apps import apps
from .api import ChapaAPI
import json

from shop_app.models import CartItem,Cart
from decimal import Decimal


@csrf_exempt
def chapa_webhook(request):
    try:
        data = json.loads(request.body)
    except json.decoder.JSONDecodeError:
        return JsonResponse(
            {
                'error': "Invalid Json Body"
            },
            status=400
        )
    
    model_class = apps.get_model(settings.CHAPA_TRANSACTION_MODEL)
    try:
        transaction_instance = model_class.objects.get(id=data.get('trx_ref'))
        transaction_instance.status = data.get('status')
        transaction_instance.response_dump = data
        transaction_instance.save()
        return JsonResponse(data)
    except model_class.DoesNotExist:
        return JsonResponse(
            {
                'error': "Invalid Transaction"
            },
            status=400
        )
    

@csrf_exempt

def initialize_payment(request):
    if request.method == "POST":
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body)
            print("Received data:", data)  # Debugging line
            
            cart_code = data.get("cart_code")
            cart = Cart.objects.get(cart_code=cart_code, paid=False)

            sub_total = sum(item.quantity * item.product.price for item in cart.items.all())  # Fixed here
            tax = Decimal("4.00")
            total_amount = sub_total + tax

            

            # Prepare data for the transaction
            amount = float(total_amount) # Should be a Decimal type
            currency = data.get('currency', 'ETB')
            email = data.get('email')
            phone_number = data.get('phone_number')
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            payment_title = data.get('payment_title', 'Payment')
            description = data.get('description')

            # Validate required fields
            if not all([amount, email, first_name, last_name]):
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            # Create a transaction record
            transaction = ChapaTransaction(
                amount= amount, 
                currency=currency,
                email=email,
                phone_number=phone_number,
                first_name=first_name,
                last_name=last_name,
                payment_title=payment_title,
                description=description
            )
            transaction.save()

            # Send request to Chapa API
            chapa_response = ChapaAPI.send_request(transaction)
            print("Chapa response:", chapa_response)  # Debugging line

            if chapa_response.get("status") == "success":
                checkout_url = chapa_response["data"].get("checkout_url")
                return JsonResponse({"checkout_url": checkout_url}, status=200)
            
            return JsonResponse({"error": "Failed to initialize payment"}, status=500)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON payload"}, status=400)
        except CartItem.DoesNotExist:
            return JsonResponse({"error": "Cart not found"}, status=404)
        except Exception as e:
            print("Unexpected error:", e)  # Debugging line for unexpected errors
            return JsonResponse({"error": "Internal server error"}, status=500)
    
    return JsonResponse({"error": "Invalid request"}, status=400)
