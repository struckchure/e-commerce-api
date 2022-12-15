from rest_framework import status
from rest_framework.response import Response

from core.services.platform_payment_service import PaystackService
from e_commerce.decorators import handle_errors
from e_commerce.utils import BaseView


class PaystackWebhookAPI(BaseView):
    @handle_errors()
    def post(self, request):
        verify_payment = PaystackService.verify_payment(request.data)

        return Response(
            data=verify_payment,
            status=status.HTTP_202_ACCEPTED,
        )
