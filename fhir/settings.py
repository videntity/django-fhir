#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

"""
BlueButtonFHIR_API
FILE: django-fhir.settings
Created: 1/9/16 11:58 AM


Create settings that can be overriden with an alternative package

"""
import os
from django.conf import settings
from importlib import import_module

__author__ = 'Mark Scrimshire:@ekivemark'


# You can override this default by replicating DJANGO_FHIR_CONFIG in your apps
# settings.py. The only restriction is to create your pluggable replacement for
# fhir_io_mongo as a top level module in your application.
# We also encourage you to follow the fhir_io_{backend_name} convention
# The pluggable backend should replicate all of the functions included in the default
# fhir_io_mongo or fhir_io_hapi pluggable modules.

DJANGO_FHIR_CONFIG = {
    "DF_APPS": ('fhir_io_mongo',),
}


DJANGO_FHIR_CONFIG.update(getattr(settings, 'DJANGO_FHIR_CONFIG', {}))

for df_app in DJANGO_FHIR_CONFIG['DF_APPS']:
    if settings.DEBUG:
        print("Module:",df_app)

    FHIR_BACKEND = import_module(df_app)

    if settings.DEBUG:
        print("django-FHIR Pluggable Module:", FHIR_BACKEND)

    if df_app not in settings.INSTALLED_APPS:
        if settings.DEBUG:
            print("Adding %s to INSTALLED_APPS" % df_app)
        settings.INSTALLED_APPS += (df_app, )

    if settings.DEBUG:

        result = getattr(FHIR_BACKEND,'hello_world')("search", "Patient", "1")
        print("")
        print("Testing Pluggable Module %s via hello world:" % FHIR_BACKEND)
        print("Answer from Hello World:", result)
