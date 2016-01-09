from django.shortcuts import render
from ..models import SupportedResourceType
from collections import OrderedDict
from django.http import HttpResponse
import json
from ..utils import (kickout_404, kickout_403, kickout_400)


def search(request, resource_type):
    try:
        rt = SupportedResourceType.objects.get(resource_name=resource_type)
        if rt.access_denied(access_to_check="fhir_search"):
            msg = "%s access denied to %s records on this FHIR server." % ("SEARCH",
                                                                           resource_type)
            return kickout_403(msg)

    except SupportedResourceType.DoesNotExist:
        msg = "%s is not a supported resource type on this FHIR server." % (resource_type)
        return kickout_404(msg)


    """Search Interaction"""
    # Example client use in curl:
    # curl -X GET  http://127.0.0.1:8000/fhir/Practitioner?foo=bar
    if request.method != 'GET':
        msg = "HTTP method %s not supported at this URL." % (request.method)
        return kickout_400(msg)
    
    od = OrderedDict()
    od['request_method']= request.method
    od['interaction_type'] = "search"
    od['resource_type']    = resource_type
    od['search_params'] = request.GET
    od['note'] = "This is only a stub for future implementation"
    
    return HttpResponse(json.dumps(od, indent=4),
                        content_type="application/json")
