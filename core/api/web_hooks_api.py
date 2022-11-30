from e_commerce.utils import BaseView
from e_commerce.decorators import handle_errors
from rest_framework.response import Response
from rest_framework import status
from core.services.platform_payment_service import PaystackService


class PaystackWebhookAPI(BaseView):
    @handle_errors()
    def post(self, request):
        verify_payment = PaystackService.verify_payment(request.data)

        return Response(
            data=verify_payment,
            status=status.HTTP_202_ACCEPTED,
        )
