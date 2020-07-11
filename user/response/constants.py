"""
Created at 11/07/20
@author: virenderkumarbhargav
"""
from enum import Enum


class TemplateError:
    def __init__(self, error_code, msg, description=None):
        self.error_code = error_code
        self.msg = msg
        self.description = description


class ErrorTemplate(Enum):
    UNKNOWN_EXCEPTION = TemplateError("ACC_000", "Unspecified Exception")
    MISSING_FIELDS = TemplateError("ACC_001", "Mandatory Fields Missing")
    ADMIN_LOGIN_ERROR = TemplateError("ACC_002", "Admin Login Required.", "Unauthorised")
    PERMISSION_ERROR = TemplateError("ACC_003", "User doesn't have required permission.", "Permission Denied")
    INTERNAL_SERVER_ERROR = TemplateError("ACC_004", "Some Internal Server Error Occurred.", "Internal Server Error")
    NOT_FOUND = TemplateError("ACC_005", "Not Found", "Required entity could not be found. Please try later.")
    INVALID_JSON = TemplateError("ACC_006", "Invalid JSON", "Invalid JSON")
    METHOD_NOT_ALLOWED = TemplateError("ACC_007", "Method Not Allowed")
    INVALID_REQUEST_BODY = TemplateError("ACC_008", "Invalid request body")
    USER_ALREADY_EXISTS = TemplateError("ACC_008", "User already exists")
