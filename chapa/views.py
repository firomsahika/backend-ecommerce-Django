from django.shortcuts import render
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.apps import apps
import json
from .models import ChapaTransaction
from .api import ChapaAPI



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
        data = json.loads(request.body)

        transaction = ChapaTransaction.objects.create(
            amount=data["amount"],
            currency="ETB",
            email=data["email"],
            phone_number=data["phone_number"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            payment_title="Chapa Payment",
            description="Payment for services",
        )

        chapa_response = ChapaAPI.send_request(transaction)

        if chapa_response.get('status')=="success":
            checkout_url = chapa_response["data"]["checkout_url"]
            return JsonResponse({"checkout_url": checkout_url}, status=200)
        return JsonResponse({"error": "Failed to initialize payment"}, status=500)
    
    return JsonResponse({"error": "Invalid request"}, status=400)