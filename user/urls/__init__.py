"""
Created at 11/07/20
@author: virenderkumarbhargav
"""
from __future__ import absolute_import

from django.conf.urls import url, include
# -*- coding: utf-8 -*-
from rest_framework.routers import SimpleRouter

from user import views

app_name = 'community'

router = SimpleRouter()  # pylint: disable=invalid-name
# router.register(r'users', views.UserViewSet, basename='users')


urlpatterns = [
    url(r'^', include(router.urls)),
]
