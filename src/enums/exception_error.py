from enum import Enum


class ExceptionError(Enum):
    USER_NOT_FOUND = "User not found"
    DATA_NOT_FOUND = "Data not found"
    INVALID_CREDENTIALS = "Invalid credentials"
    UNAUTHORIZED = "Unauthorized"
    FORBIDDEN = "Forbidden"
    INTERNAL_ERROR = "Internal error"
    TOKEN_EXPIRED = "Token expired"
    TOKEN_INVALID = "Token invalid"
