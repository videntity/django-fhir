#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

"""
BlueButtonFHIR_API
FILE: fhir_io_hapi.models
Created: 1/7/16 10:40 AM

Create a model linked to SupportedResourceType

We should probably follow the User Application Model in Django
and Django_OAuth_Toolkit to allow
Customized extensions to the core model.

For now we will link on resource_name.

"""
__author__ = 'Mark Scrimshire:@ekivemark'

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from fhir.models import SupportedResourceType

# See link below for porting advice for Python 2 to 3
# https://docs.djangoproject.com/en/1.9/topics/python3/


@python_2_unicode_compatible
class ResourceTypeControl(models.Model):
    resource_name           = models.ForeignKey(SupportedResourceType)
    apply_patient_filter    = models.BooleanField(help_text="Does this resource need to mask "
                                                            "patient ids?")
    force_url_id_override   = models.BooleanField(help_text="Does URI need to be overridden "
                                                            "in order to prevent retreiving "
                                                            "other people's data?")
    search_parameter_mask   = models.TextField(max_length=5120, default="",
                                        help_text="Empty string indicates no mask. "
                                                  "Create list of "
                                                  "search parameters to block")

    # Python2 uses __unicode__(self):
    def __str__(self):
        return self.resource_name.resource_name

    def parameter_restriction(self):
        return self.search_parameter_mask.split(",")

    # Save json to search_parameter_mask using:
    # ResourceTypeControl.search_parameter_mask = json.dumps(listToBeStored)

    def patient_filter(self):
        return self.apply_patient_filter

    def url_id_override(self):
        return self.force_url_id_override
