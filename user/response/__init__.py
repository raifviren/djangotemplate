"""
Created at 11/07/20
@author: virenderkumarbhargav
"""
from rest_framework.response import Response

from .constants import ErrorTemplate, TemplateError


class ResponseWrapper(Response):

    def __init__(self, data, status, **kwargs):
        super(ResponseWrapper, self).__init__(data=data, status=status, headers={'Content-Type': 'application/json'},
                                              **kwargs)

    def __repr__(self):
        return self.data

    @classmethod
    def response(cls, data, status):
        """
        Example usage:
        ResponseWrapper.response({'message': "Success"}, status.HTTP_200_OK)

        response is a utility function to output the final JSON response created using the params

        @param data: dict final Json Response to be sent
        @param status: int Http Status Code
        @return: Response object

        """
        if 200 <= status <= 207:
            result = {
                "data": data,
                "error": {}
            }
        # logger.debug('RESPONSE ' + str(data) + "" + str(status))
        return cls(data, status=status)

    @classmethod
    def error_response(cls, status, error_template, *args, **kwargs):
        """
        error_response is a utility function to output the final JSON response in error cases.

        Example usage:
        ResponseWrapper.error_response(status.HTTP_400_BAD_REQUEST, ErrorTemplate.NOT_FOUND, "requestId: {}".format(reference_id))


        @param status: int Http Status Code
        @param error_template: an instance of ErrorTemplate Enum
        @param args: list list of string to form ';' separated error_detail
        @return: Response object

        """
        if not isinstance(error_template.value, TemplateError):
            raise Exception("Invalid Error Template")
        error_detail = str(error_template.value.description) if error_template.value.description is not None else ""
        error_detail += ";".join(args)
        result = {
            "data": {},
            "error": {
                "error_code": str(error_template.value.error_code),
                "error_message": str(error_template.value.msg),
                "error_detail": error_detail,
                "meta_data": kwargs.get('meta_data', None)
            }

        }
        # logger.error('RESPONSE ' + str(result))
        return cls(result, status)

    @classmethod
    def error_serializer_response(cls, status, serializer, **kwargs):
        """
        Utility function to output the final JSON response using Serializer's error strings obtained through its validation phase

        Example usage:
        if not serializer.is_valid():
            return ResponseWrapper.error_serializer_response(status.HTTP_400_BAD_REQUEST, serializer)
        @param status: int Http Status Code
        @param serializer: DRF Serializer instance
        @return: Response object

        """
        result = {
            "data": {},
            "error": {
                "error_code": ErrorTemplate.INVALID_REQUEST_BODY.value.error_code,
                "error_message": ErrorTemplate.INVALID_REQUEST_BODY.value.msg,
                "error_detail": serializer.errors,
                "meta_data": kwargs.get('meta_data', None)
            }
        }
        return cls(result, status)


__all__ = ResponseWrapper
