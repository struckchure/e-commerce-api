from rest_framework import status
from rest_framework.response import Response

from core.services.payment_service import PaymentPlaformService
from e_commerce.decorators import handle_errors
from e_commerce.permissions import IsStaff
from e_commerce.utils import BaseView


class ListCreatePaymentPlatformAPI(BaseView):

    permission_classes = [
        IsStaff,
    ]

    @handle_errors()
    def get(self, request):
        payment_platform_list = PaymentPlaformService.list_payment_platforms(
            search=request.query_params.get("search"),
            skip=int(request.query_params.get("skip", 0)),
            limit=int(request.query_params.get("limit", 10)),
        )

        return Response({"data": payment_platform_list}, status=status.HTTP_200_OK)

    @handle_errors()
    def post(self, request):
        payment_platform = PaymentPlaformService.create_payment_platform(
            name=request.data.get("name"),
            platform=request.data.get("platform"),
            credentials=request.data.get("credentials"),
            active=request.data.get("active"),
            added_by=request.user.id,
        )

        return Response({"data": payment_platform}, status=status.HTTP_201_CREATED)


class GetUpdateDeletePaymentPlatformAPI(BaseView):

    permission_classes = [
        IsStaff,
    ]

    @handle_errors()
    def get(self, request, payment_platform_id):
        payment_platform = PaymentPlaformService.get_payment_platform(
            payment_platform_id
        )

        return Response({"data": payment_platform}, status=status.HTTP_200_OK)

    @handle_errors()
    def put(self, request, payment_platform_id):
        payment_platform = PaymentPlaformService.update_payment_platform(
            id=payment_platform_id,
            name=request.data.get("name"),
            platform=request.data.get("platform"),
            active=request.data.get("active"),
            credentials=request.data.get("credentials"),
        )

        return Response({"data": payment_platform}, status=status.HTTP_200_OK)

    @handle_errors()
    def delete(self, request, payment_platform_id):
        PaymentPlaformService.delete_payment_platform(id=payment_platform_id)

        return Response(status=status.HTTP_204_NO_CONTENT)
