#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

"""
BlueButtonFHIR_API
FILE: django-fhir.settings
Created: 1/9/16 11:58 AM


Create settings that can be overriden with an alternative package

"""
from django.conf import settings

__author__ = 'Mark Scrimshire:@ekivemark'


# You can override this default by replicating DJANGO_FHIR_CONFIG in your apps
# settings.py. The only restriction is to create your pluggable replacement for
# fhir_io_mongo as a top level module in your application.
# We also encourage you to follow the fhir_io_{backend_name} convention
# The pluggable backend should replicate all of the functions included in the default
# fhir_io_mongo or fhir_io_hapi pluggable modules.

DJANGO_FHIR_CONFIG = {
    "DF_APPS": {'fhir_io_mongo',
                }
}


DJANGO_FHIR_CONFIG.update(getattr(settings, 'DJANGO_FHIR_CONFIG', {}))

for df_app in DJANGO_FHIR_CONFIG['DF_APPS']:

    FHIR_BACKEND = __import__(df_app)
    if settings.DEBUG:
        print("django-FHIR Pluggable Module:", FHIR_BACKEND)

    if df_app not in settings.INSTALLED_APPS:
        settings.INSTALLED_APPS += (df_app, )

    if settings.DEBUG:
        result = FHIR_BACKEND.hello_world("search", "Patient", "1" )
        print("Testing Pluggable Module %s via hello world:" % FHIR_BACKEND)
        print("Answer from Hello World:", result)
