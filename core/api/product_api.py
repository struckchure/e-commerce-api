from core.services.product_service import ProductService
from e_commerce.decorators import handle_errors
from e_commerce.permissions import IsStaffOrReadOnly
from e_commerce.utils import BaseView, remove_none_values
from rest_framework import status
from rest_framework.response import Response

product_service = ProductService()


class ListCreateAPI(BaseView):

    permission_classes = [
        IsStaffOrReadOnly,
    ]

    @handle_errors()
    def get(self, request):
        search = request.query_params.get("search")
        skip = request.query_params.get("skip")
        limit = request.query_params.get("limit")

        kwargs = remove_none_values({"search": search, "skip": skip, "limit": limit})

        return Response(
            {"data": product_service.list_product(**kwargs)}, status=status.HTTP_200_OK
        )

    @handle_errors()
    def post(self, request):
        name = request.data.get("name")
        description = request.data.get("description")
        images = request.data.getlist("images")
        price = request.data.get("price")
        stock = request.data.get("stock")
        category = request.data.get("category")
        tags = request.data.getlist("tags")

        return Response(
            {
                "data": product_service.create_product(
                    name=name,
                    description=description,
                    images=images,
                    price=price,
                    stock=stock,
                    category=category,
                    tags=tags,
                )
            },
            status=status.HTTP_201_CREATED,
        )


class GetUpdateDeleteAPI(BaseView):

    permission_classes = [
        IsStaffOrReadOnly,
    ]

    @handle_errors()
    def get(self, request, id):
        return Response(
            {"data": product_service.get_product(id)}, status=status.HTTP_200_OK
        )

    @handle_errors()
    def put(self, request, id):
        name = request.data.get("name")
        description = request.data.get("description")
        images = request.data.get("images")
        price = request.data.get("price")
        stock = request.data.get("stock")
        category = request.data.get("category")
        tags = request.data.get("tags")

        return Response(
            {
                "data": product_service.update_product(
                    id=id,
                    name=name,
                    description=description,
                    images=images,
                    price=price,
                    stock=stock,
                    category=category,
                    tags=tags,
                )
            },
            status=status.HTTP_200_OK,
        )

    @handle_errors()
    def delete(self, request, id):
        product_service.delete_product(id)

        return Response(status=status.HTTP_204_NO_CONTENT)
