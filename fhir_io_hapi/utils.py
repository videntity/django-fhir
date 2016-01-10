#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

"""
BlueButtonFHIR_API
FILE: fhir_io_hapi.utils
Created: 1/7/16 11:41 AM

utilities used module-wide

"""
import json

from collections import OrderedDict

from xml.etree.ElementTree import Element, tostring

from apps.v1api.models import Crosswalk

from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse

__author__ = 'Mark Scrimshire:@ekivemark'


def build_params(get, skip_parm=['_id','_format']):
    """
    Build the URL Parameters.
    We have to skip any in the skip list.

    :param get:
    :return:
    """
    # We will default to json for content handling
    in_fmt = "json"

    pass_to = ""

    url_param = get_url_query_string(get, skip_parm)

    if "_format" in skip_parm:
        print("skip_parm dropped _format - url_param now:", url_param)

        # Check for _format and process in this section
        get_fmt = get_format(get)
        if settings.DEBUG:
            print("get_Format returned:", get_fmt)

        #get_fmt_type = "?_format=xml"
        #get_fmt_type = "?_format=json"

        if get_fmt:
            get_fmt_type = "_format=" + get_fmt

            pass_to = "?" + get_fmt_type
        else:
            if settings.DEBUG:
                print("Get Format:[", get_fmt, "]")
            in_fmt_type = "_format=" + in_fmt
            pass_to = "?" + in_fmt_type

    if len(url_param) > 1:
        if settings.DEBUG:
            print("URL Params = ", url_param)
        if "?" in pass_to:
            # We already have the start of a query string in the url
            # So we prefix with "&"
            pass_to = pass_to + "&" + url_param
        else:
            # There is no ? so we need to start the query string
            pass_to = pass_to + "?" + url_param
    if settings.DEBUG:
        print("URL Pass_To:", pass_to)

    return pass_to


def concat_string(target, msg=[], delimiter="", last=""):
    """
    Concatenate a series of strings to the end of the target
    Delimiter is optional filler between items
    :param target:
    :param msg:
    :return: target
    """

    result = target

    for m in msg[:-1]:
        result = result + m + delimiter

    result = result + msg[-1] + last

    return result


def crosswalk_id(request, id=None, element='fhir_url_id'):
    # Lookup up in Crosswalk with request.user
    # First we need to check for AnonymousUser

    if request.user.id == None:
        if settings.DEBUG:
            print('Sorry - AnonymousUser gets no information')
        return None
    elif settings.DEBUG:
        print("lookup_xwalk:Request User Beneficiary(Patient):",
              request.user)
    else:
        pass

    try:
        xwalk = Crosswalk.objects.get(user=request.user)
    except Crosswalk.DoesNotExist:
        messages.error(request, "Unable to find Patient ID")
        return None

    if element.lower() == 'fhir_url_id' and xwalk.fhir_url_id == "":

        err_msg = ['Sorry, We were unable to find',
                   'your record', ]
        exit_message = concat_string("",
                                     msg=err_msg,
                                     delimiter=" ",
                                     last=".")
        messages.error(request,
                       exit_message)
        return None

    else:
        if settings.DEBUG:
            print("We got a match on ",
                  request.user,
                  ":",
                  xwalk.fhir_url_id)

        return xwalk.fhir_url_id


def dict_to_xml(tag, d):
    '''
    Turn a simple dict of key/value pairs into XML
    '''
    elem = Element(tag)
    for key, val in d.items():
        child = Element(key)
        child.text = str(val)
        elem.append(child)
    return elem


def error_status(r, status_code=404, reason="undefined error occured"):
    """
    Generate an error page
    based on fhir.utils.kickout_xxx
    :param reason:
    :param status_code:
    :return:
    """
    error_detail = r.text
    if settings.DEBUG:
        if r.text[0] == "<":
            error_detail = "xml:"
            error_detail += r.text
        else:
            error_detail = r.json()

    if reason == "undefined error occured":
        if status_code == 404:
            reason = "page not found"
        elif status_code == 403:
            reason = "You are not authorised to access this page. Do you need to login?"
        elif status_code == 400:
            reason = "There was a problem with the data"
        elif status_code == 301:
            reason = "The requested page has been permanently moved"

    response= OrderedDict()

    response["errors"] = [reason, error_detail]
    response["code"] = status_code

    return HttpResponse(json.dumps(response, indent = 4),
                        status=status_code,
                        content_type="application/json")
