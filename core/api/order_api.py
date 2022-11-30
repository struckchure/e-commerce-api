from rest_framework.response import Response
from rest_framework import status
from e_commerce.utils import BaseView
from e_commerce.decorators import handle_errors
from e_commerce.permissions import IsAuthenticated
from core.services.order_service import OrderService


class ListOrderAPI(BaseView):

    permission_classes = [
        IsAuthenticated,
    ]

    @handle_errors()
    def get(self, request):
        user_id = request.user.id
        skip = request.query_params.get("skip", 0)
        limit = request.query_params.get("limit", 10)

        return Response(
            {"data": OrderService.list_orders(user_id=user_id, skip=skip, limit=limit)},
            status=status.HTTP_200_OK,
        )


class GetOrderAPI(BaseView):

    permission_classes = [
        IsAuthenticated,
    ]

    @handle_errors()
    def get(self, request, order_id):
        return Response(
            {"data": OrderService.get_order(order_id=order_id)},
            status=status.HTTP_200_OK,
        )
