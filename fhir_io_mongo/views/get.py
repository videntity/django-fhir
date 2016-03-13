#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

"""
BlueButtonFHIR_API
FILE: django-fhir.fhir_io_mongo.views.get
Created: 1/9/16 3:57 PM


"""
import json

from collections import OrderedDict

from django.http import HttpResponse

__author__ = 'Mark Scrimshire:@ekivemark'


def hello_world(request, resource_type, id, *arg, **kwargs):
    """
    Simple Hello World to check for plugable module
    :param request:
    :param resource_type:
    :param id:
    :param arg:
    :param kwargs:
    :return:
    """
    return "Hello World from fhir_io_mongo.views.get.hello_world: %s,{%s}[%s]" % (request,
                                                                               resource_type,
                                                                               id)


def read(request, resource_type, id, *arg, **kwargs):
    """
    Read from remote FHIR Server
    :param resourcetype:
    :param id:
    :return:
    """

    od = OrderedDict()
    od['request_method']= request.method
    od['interaction_type'] = "search"
    od['resource_type']    = resource_type
    od['search_params'] = request.GET
    od['note'] = "This is only a stub for future implementation of " \
                 "MongoDB as a pluggable module for django-fhir"

    return HttpResponse(json.dumps(od, indent=4),
                        content_type="application/json")
