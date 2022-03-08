#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2018-2-10

@author: qi
'''
from django.urls import path, re_path
from . import views

app_name = 'wopiserver'
urlpatterns = [
    path('files', views.wopiGetFileInfo),
    path('files/contents', views.wopiFileContents),
]

