from core.services.cart_service import CartService
from e_commerce.decorators import handle_errors
from e_commerce.permissions import IsAuthenticated, IsObjectOwner
from e_commerce.utils import BaseView
from rest_framework import status
from rest_framework.response import Response


class ListCreateCartItemAPI(BaseView):

    permission_classes = [
        IsAuthenticated,
    ]

    @handle_errors()
    def get(self, request):
        user_id = request.user.id
        skip = request.query_params.get("skip")
        limit = request.query_params.get("limit")

        return Response(
            {"data": CartService().list_items(user_id, skip, limit)},
            status=status.HTTP_200_OK,
        )

    @handle_errors()
    def post(self, request):
        user_id = request.user.id
        product_id = request.data.get("product")
        quantity = request.data.get("quantity")

        item = CartService().add_item(user_id, product_id, quantity)

        return Response({"data": item}, status=status.HTTP_201_CREATED)


class GetUpdateDeleteCartItemAPI(BaseView):

    permission_classes = [
        IsObjectOwner,
    ]

    def get_object(self):
        item_id = self.kwargs.get("item_id")

        obj = CartService().get_item(item_id)
        self.check_object_permissions(self.request, obj["user"]["id"])

        return obj

    @handle_errors()
    def get(self, request, item_id):
        return Response({"data": self.get_object()}, status=status.HTTP_200_OK)

    @handle_errors()
    def put(self, request, item_id):
        self.get_object()

        quantity = request.data.get("quantity")

        return Response(
            {"data": CartService().update_item(item_id, quantity)},
            status=status.HTTP_200_OK,
        )

    @handle_errors()
    def delete(self, request, item_id):
        self.get_object()

        CartService().delete_item(item_id)

        return Response(status=status.HTTP_204_NO_CONTENT)
