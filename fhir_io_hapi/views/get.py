#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

"""
django-fhir
FILE: get
Created: 1/6/16 5:08 PM


"""
import json
import requests

from collections import OrderedDict
from xml.dom import minidom
from xml.etree.ElementTree import tostring

from ..utils import (build_params,
                     crosswalk_id,
                     dict_to_xml,
                     error_status,
                     check_rt_controls)
from ..models import ResourceTypeControl

from fhir.models import SupportedResourceType

from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.http import (HttpResponseRedirect,
                         HttpResponse,)
from django.shortcuts import render

from fhir.utils import (kickout_404)
from fhir.views.utils import check_access_interaction_and_resource_type

__author__ = 'Mark Scrimshire:@ekivemark'


def hello_world(request, resource_type, id):
    """
    Simple Hello World to check for plugable module activation
    :param request:
    :param resource_type:
    :param id:
    :param arg:
    :param kwargs:
    :return:
    """

    od = OrderedDict()
    od['request']= request
    od['interaction_type'] = ""
    od['resource_type']    = resource_type
    od['id'] = id
    od['format'] = "json"
    od['note'] = "Hello World from fhir_io_hapi.get.hello_world: %s,{%s}[%s]" % (request,
                                                                        resource_type,
                                                                        id)

    return "Hello World from fhir_io_hapi.get.hello_world: %s,{%s}[%s] %s" % (request,
                                                                              resource_type,
                                                                              id, od)


def read(request, resource_type, id, *args, **kwargs):
    """
    Read from remote FHIR Server
    :param resourcetype:
    :param id:
    :return:


    # Example client use in curl:
    # curl  -X GET http://127.0.0.1:8000/fhir/Practitioner/1234

    """

    interaction_type = 'read'

    read = generic_read(request, interaction_type, id, vid, *args, **kwargs)

    return read


def history(request, resource_type, id, *args, **kwargs):
    """
    History specific read
    GET [base]/[type]/[id]/_history/ {?_format=[mime-type]}
    """
    interaction_type = '_history'

    history = generic_read(request, interaction_type, resource_type, id, vid=None, *args, **kwargs)

    return history


def vread(request, resource_type, id, vid, *args, **kwargs):
    """
    Version specific read
    GET [base]/[type]/[id]/_history/[vid] {?_format=[mime-type]}
    """
    interaction_type = 'vread'

    vread = generic_read(request, interaction_type, resource_type, id, vid, *args, **kwargs)

    return vread


def generic_read(request, interaction_type, resource_type, id, vid=None, *args, **kwargs):
    """
    Read from remote FHIR Server
    :param resourcetype:
    :param id:
    :return:


    # Example client use in curl:
    # curl  -X GET http://127.0.0.1:8000/fhir/Practitioner/1234

    """

    # interaction_type = 'read' or '_history' or 'vread'
    if settings.DEBUG:
        print("interaction_type:", interaction_type)
    #Check if this interaction type and resource type combo is allowed.
    deny = check_access_interaction_and_resource_type(resource_type, interaction_type)
    if deny:
        #If not allowed, return a 4xx error.
        return deny

    srtc = check_rt_controls(resource_type)
    # We get back an Supported ResourceType Control record or None

    if settings.DEBUG:
        if srtc:
            print("Parameter Rectrictions:", srtc.parameter_restriction())
        else:
            print("No Resource Controls found")

    if srtc:
        if srtc.force_url_id_override:
            key = crosswalk_id(request, id)
            # Crosswalk returns the new id or returns None
            if settings.DEBUG:
                print("crosswalk:", key)
        else:
            # No Id_Overide so use the original id
            key = id
    else:
        key = id

    # Do we have a key?
    if key == None:
        return kickout_404("FHIR_IO_HAPI:Search needs a valid Resource Id that is linked "
                           "to the authenticated user "
                           "(%s) which was not available" % request.user)

    # Now we get to process the API Call.

    if settings.DEBUG:
        print("Now we need to evaluate the parameters and arguments"
              " to work with ", key, "and ", request.user)
        print("GET Parameters:", request.GET, ":")

    mask = False
    if srtc:
        if srtc.force_url_id_override:
            mask = True

    in_fmt = "json"
    Txn = {'name': resource_type,
           'display': resource_type,
           'mask': mask,
           'server': settings.FHIR_SERVER,
           'locn': "/baseDstu2/"+resource_type+"/",
           'in_fmt': in_fmt,
           }

    skip_parm = []
    if srtc:
        skip_parm = srtc.parameter_restriction()

    #skip_parm = ['_id',
    #             'access_token', 'client_id', 'response_type', 'state']

    if settings.DEBUG:
        print('Masking the following parameters', skip_parm)
    # access_token can be passed in as a part of OAuth protected request.
    # as can: state=random_state_string&response_type=code&client_id=ABCDEF
    # Remove it before passing url through to FHIR Server

    pass_params = build_params(request.GET, skip_parm)
    if settings.DEBUG:
        print("Parameters:", pass_params)

    if interaction_type == "vread":
        pass_to = Txn['server'] + Txn['locn'] + key + "/" + "_history" + "/" + vid
    elif interaction_type == "_history":
        pass_to = Txn['server'] + Txn['locn'] + key + "/" + "_history"
    else:  # interaction_type == "read":
        pass_to = Txn['server'] + Txn['locn'] + key + "/"

    print("Here is the URL to send, %s now get parameters %s" % (pass_to,pass_params))

    if pass_params != "":
        pass_to = pass_to + pass_params

    # Now make the call to the backend API
    try:
        r = requests.get(pass_to)

    except requests.ConnectionError:
        if settings.DEBUG:
            print("Problem connecting to FHIR Server")
        messages.error(request, "FHIR Server is unreachable." )
        return HttpResponseRedirect(reverse_lazy('api:v1:home'))

    if r.status_code in [301, 302, 400, 403, 404, 500]:
        return error_status(r, r.status_code)

    text_out = ""
    print("r:", r.text)

    if '_format=xml' in pass_params:
        text_out= minidom.parseString(r.text).toprettyxml()
    else:
        text_out = r.json()

    od = OrderedDict()
    od['request_method']= request.method
    od['interaction_type'] = interaction_type
    od['resource_type']    = resource_type
    od['id'] = key
    if vid != None:
        od['vid'] = vid

    if settings.DEBUG:
        print("Query List:", request.META['QUERY_STRING'] )

    od['parameters'] = request.GET.urlencode()

    if settings.DEBUG:
        print("or:", od['parameters'])

    if '_format=xml' in pass_params.lower():
        fmt = "xml"
    elif '_format=json' in pass_params.lower():
        fmt = "json"
    else:
        fmt = ''
    od['format'] = fmt
    od['bundle'] = text_out
    od['note'] = 'This is the %s Pass Thru (%s) ' % (resource_type,key)

    if settings.DEBUG:
        od['note'] += 'using: %s ' % (pass_to)
        print(od)

    if od['format'] == "xml":
        if settings.DEBUG:
            print("We got xml back in od")
        return HttpResponse( tostring(dict_to_xml('content', od)),
                             content_type="application/%s" % od['format'])
    elif od['format'] == "json":
        if settings.DEBUG:
            print("We got json back in od")
        return HttpResponse(json.dumps(od, indent=4),
                            content_type="application/%s" % od['format'])

    if settings.DEBUG:
        print("We got a different format:%s" % od['format'])
    return render(request,
                  'fhir_io_hapi/default.html',
                  {'content': json.dumps(od, indent=4),
                   'output': od},
                  )
