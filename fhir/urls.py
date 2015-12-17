#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url

from .views.create import create
from .views.rud import read_or_update_or_delete
from .views.search import search
from .views.history import history
urlpatterns = patterns('',
    
    #Interactions on Resources
    
    
    #History GET ------------------------------
    url(r'(?P<resource_type>[^/]+)/(?P<id>[^/]+)/_history', history,
        name='fhir_history'),
    
    # ---------------------------------------
    # Read GET
    # Update PUT
    # Delete DELETE
    # ---------------------------------------
    url(r'(?P<resource_type>[^/]+)/(?P<id>[^/]+)',
        read_or_update_or_delete,
        name='fhir_read_or_update_or_delete'),
    
    


    
    
    #Search  GET ------------------------------
    url(r'(?P<resource_type>[^/]+)?', search,
        name='fhir_search'),
    
    #Create  POST ------------------------------
    url(r'(?P<resource_type>[^/]+)', create,
        name='fhir_create'),




    
    )
