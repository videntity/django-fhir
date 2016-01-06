#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

"""
django-fhir
FILE: .views.hello
Created: 1/6/16 3:44 PM


"""
from django.http import HttpResponse

__author__ = 'Mark Scrimshire:@ekivemark'


def hello(request, *args, **kwargs):
    """
    A simple hello world test for the fhir package
    :param request:
    :param args:
    :param kwargs:
    :return:
    """

    return HttpResponse('Hello, from django-fhir ! %s' % kwargs)