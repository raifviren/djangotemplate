"""
Created at 11/07/20
@author: virenderkumarbhargav
"""
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.pagination import PageNumberPagination

from user.exceptions import BaseInputError, BaseServerError
from user.response import ResponseWrapper, ErrorTemplate


class BaseReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    @summary: This Viewset can be used to create viewset that only support Get call
    """
    PageNumberPagination.page_size = 10
    pagination_class = PageNumberPagination


class BaseViewSet(viewsets.ModelViewSet):
    PageNumberPagination.page_size = 10
    pagination_class = PageNumberPagination

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return ResponseWrapper.response(serializer.data, status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
        Overwrites default create method.
        """
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return ResponseWrapper.error_serializer_response(status.HTTP_412_PRECONDITION_FAILED, serializer)
        try:
            if request.user and request.user.is_authenticated:
                serializer.validated_data['created_by'] = self.request.user
            result = serializer.create(validated_data=serializer.validated_data)
            return ResponseWrapper.response(self.serializer_class(result).data, status=status.HTTP_201_CREATED)
        except BaseInputError as exception:
            print(exception)
            return ResponseWrapper.error_response(status.HTTP_400_BAD_REQUEST, ErrorTemplate.INVALID_REQUEST_BODY,
                                                  exception.args[0])
        except BaseServerError as exception:
            print(exception)
            return ResponseWrapper.error_response(status.HTTP_500_INTERNAL_SERVER_ERROR,
                                                  ErrorTemplate.INTERNAL_SERVER_ERROR, exception.args[0])

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = get_object_or_404(self.get_queryset(), pk=self.kwargs['pk'])
            self.check_object_permissions(self.request, instance)
            serializer = self.get_serializer(instance)
            return ResponseWrapper.response(serializer.data, status.HTTP_200_OK)
        except BaseInputError as exception:
            print(exception)
            return ResponseWrapper.error_response(status.HTTP_400_BAD_REQUEST, ErrorTemplate.INVALID_REQUEST_BODY,
                                                  exception.args[0])
        except BaseServerError as exception:
            print(exception)
            return ResponseWrapper.error_response(status.HTTP_500_INTERNAL_SERVER_ERROR,
                                                  ErrorTemplate.INTERNAL_SERVER_ERROR, exception.args[0])

    def update(self, request, *args, **kwargs):
        instance = get_object_or_404(self.get_queryset(), pk=self.kwargs['pk'])
        self.check_object_permissions(self.request, instance)
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid():
            result = serializer.update(instance=instance, validated_data=request.data)
            return ResponseWrapper.response(self.serializer_class(result).data, status.HTTP_200_OK)
        else:
            return ResponseWrapper.error_serializer_response(status.HTTP_400_BAD_REQUEST, serializer)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = get_object_or_404(self.get_queryset(), pk=self.kwargs['pk'])
            self.check_object_permissions(self.request, instance)
            # self.perform_destroy(instance)
            if hasattr(instance,'is_deleted'):
                instance.is_deleted = True
                instance.save()
                return ResponseWrapper.response({'success': True}, status.HTTP_204_NO_CONTENT)
            else:
                return ResponseWrapper.error_response(status.HTTP_406_NOT_ACCEPTABLE, ErrorTemplate.PERMISSION_ERROR)
        except BaseInputError as exception:
            print(exception)
            return ResponseWrapper.error_response(status.HTTP_400_BAD_REQUEST, ErrorTemplate.INVALID_REQUEST_BODY,
                                                  exception.args[0])
        except BaseServerError as exception:
            print(exception)
            return ResponseWrapper.error_response(status.HTTP_500_INTERNAL_SERVER_ERROR,
                                                  ErrorTemplate.INTERNAL_SERVER_ERROR, exception.args[0])
