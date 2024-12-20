import requests
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from . import models


try:
    SECRET = settings.CHAPA_SECRET
    API_URL = settings.CHAPA_API_URL
    API_VERSION = settings.CHAPA_API_VERSION
    CALLBACK_URL = settings.CHAPA_WEBHOOK_URL
    TRANSACTION_MODEL = settings.CHAPA_TRANSACTION_MODEL

except AttributeError as e:
    raise ImproperlyConfigured(f"One or more chapa config missing {e}, please check in your settings file")


class ChapaAPI:
    @classmethod
    def get_headers(cls) -> dict:
        return {
            'Content-type': 'application/json',
            'Authorization': f'Bearer {SECRET}'
        }

    @classmethod
    def get_base_url(cls) -> str:
        return API_URL + '/' + API_VERSION.replace('/', '')

    @classmethod
    def send_request(cls, transaction: models.ChapaTransactionMixin, update_record=True) -> dict:
        data = {
            'amount': transaction.amount,
            'currency': transaction.currency,
            'email': transaction.email,
            'first_name': transaction.first_name,
            'last_name': transaction.last_name,
            'tx_ref': str(transaction.id),
            'callback_url': CALLBACK_URL,
            'customization[title]': transaction.payment_title,
            'customization[description]': transaction.description,
            'phone_number': transaction.phone_number,
            'redirect_url': transaction.redirect_url
        }

        transaction_url = f'{cls.get_base_url()}/transaction/initialize'
        response = requests.post(transaction_url, json=data, headers=cls.get_headers())

        try:
            response_data = response.json()
        except ValueError:
            print("Failed to parse response JSON:", response.text)  # Debugging line
            return {"status": "failed", "message": "Invalid response from Chapa"}

        if response_data.get("status") == "success" and update_record:
            transaction.status = models.ChapaStatus.PENDING
            transaction.checkout_url = response_data.get("data", {}).get("checkout_url")
            transaction.save()

        return response_data
