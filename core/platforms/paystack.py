import enum
from core.platforms.base import Platform
import requests

RECIEVE_ENDPOINT = "https://api.paystack.co/transaction/initialize/"
VERIFY_ENDPOINT = "https://api.paystack.co/transaction/verify/"


class PaystackEvents(enum.Enum):

    SUCCESS = "charge.success"
    FAILED = ""


class Paystack(Platform):
    """Paystack platform implementation."""

    def __init__(self, secret_key, public_key):
        self.secret_key = secret_key
        self.public_key = public_key

        self.headers = {"Authorization": "Bearer %s" % self.secret_key}

    def initiate_payment(self, email, amount):
        payload = {"email": email, "amount": amount * 100}

        response = requests.post(
            url=RECIEVE_ENDPOINT,
            data=payload,
            headers=self.headers,
        )

        return response.json()
