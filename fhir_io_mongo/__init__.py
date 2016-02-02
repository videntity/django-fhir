#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

"""
BlueButtonFHIR_API
FILE: __init__.py
Created: 1/9/16 3:56 PM

fhir_io_mongo must be loaded at the top level of an application.
ie. fhir_io_mongo will work but sub_directory.fhir_io_mongo fails

"""
__author__ = 'Mark Scrimshire:@ekivemark'

from .views.get import hello_world
from .views.get import read

from .settings import *


