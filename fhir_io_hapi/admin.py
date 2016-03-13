#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

"""
BlueButtonFHIR_API
FILE: fhir_io_hapi.admin
Created: 1/7/16 11:12 AM


"""
__author__ = 'Mark Scrimshire:@ekivemark'


from django.contrib import admin
from .models import ResourceTypeControl

class ResourceTypeControlAdmin(admin.ModelAdmin):

    list_display =  ('resource_name', 'search_parameter_mask' )
    search_fields = ('resource_name', )

admin.site.register(ResourceTypeControl, ResourceTypeControlAdmin)
