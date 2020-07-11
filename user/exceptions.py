"""
Created at 11/07/20
@author: virenderkumarbhargav
"""
# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class BaseAppException(Exception):
    """
    BaseAppException is the base class to inherit for all exceptions
    """
    pass


class BaseServerError(BaseAppException):
    """
    ServerError is the base class for exceptions written mainly for viewsets and
    viewset must return 500 status code if viewset encountered with those errors.
    """
    pass


class BaseInputError(BaseAppException):
    """
    InputError is the base class for exceptions written mainly for viewsets and
    viewset must return 400 status code if viewset encountered with those errors.
    """
    pass


class InvalidInputError(BaseInputError):
    """
    InputError raised when invalid input is provided
    """
    pass


class PhoneNotVerified(BaseInputError):
    """
    InputError raised when something is wrong with Facebook or Google Id
    """
    pass


class FileUploadError(BaseServerError):
    """
    InputError raised when something is wrong with Facebook or Google Id
    """
    pass
