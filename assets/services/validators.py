
from rest_framework.exceptions import ValidationError


def format_errors(errors):
    if isinstance(errors, dict):
        for field_errors in errors.values():
            if isinstance(field_errors, list) and field_errors:
                return str(field_errors[0])
            elif isinstance(field_errors, str):
                return field_errors
    elif isinstance(errors, list) and errors:
        return str(errors[0])
    return "Произошла ошибка валидации."