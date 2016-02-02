#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

"""
django-fhir
FILE: __init__.py
Created: 1/6/16 5:07 PM


"""
__author__ = 'Mark Scrimshire:@ekivemark'


# Hello World is here to test the loading of the module from fhir.settings
# from .settings import *
from .views.get import hello_world

from .views.get import (read, vread, history)

from .views.search import find