from rest_framework import status
from rest_framework.views import exception_handler


class Exception(Exception):

    message = "An Error Occured"
    code = status.HTTP_400_BAD_REQUEST

    def __init__(self, message=None, code=None):
        self.message = message or self.message or self.__doc__
        self.code = code or self.code

    def __str__(self):
        if isinstance(self.message, str):
            return self.message
        return ""

    def __dict__(self):
        if isinstance(self.message, dict):
            return self.message
        return {}


def customer_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if "detail" in response.data:
            response.data["error"] = response.data.pop("detail")

    return response
