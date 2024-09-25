from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.exceptions import ValidationError
from rest_framework import status


def exception_handler(exc, context):
    response = drf_exception_handler(exc, context)
    error_type = exc.__class__.__name__

    if isinstance(exc, ValidationError) and response is not None:
        errors = []
        for field, error_messages in response.data.items():
            for message in error_messages:
                errors.append({"field": field, "message": message})

        custom_response = {
            "success": False,
            "status": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "type": error_type,
            "errors": errors,
        }

        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY

    else:
        custom_response = {
            "success": False,
            "status": response.status_code,
            "type": error_type,
            "error": response.data.get("detail", str(exc)),
        }

    if response is not None:
        response.data = custom_response

    return response
