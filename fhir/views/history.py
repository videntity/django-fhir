from django.shortcuts import render
from ..models import SupportedResourceType
from collections import OrderedDict
from django.http import HttpResponse
import json
from ..utils import (kickout_404, kickout_403, kickout_400)

def history(request, resource_type, id):
    
    interaction_type = '_history'
    #Check if this interaction type and resource type combo is allowed.
    deny = check_access_interaction_and_resource_type(resource_type, interaction_type)
    if deny:
        #If not allowed, return a 4xx error.
        return deny


    """Read Search Interaction"""
    # Example client use in curl:
    # curl  -X GET http://127.0.0.1:8000/fhir/Practitioner/12345/_history
    if request.method != 'GET':
        msg = "HTTP method %s not supported at this URL." % (request.method)
        return kickout_400(msg)
    
    od = OrderedDict()
    od['request_method']= request.method
    od['interaction_type'] = "history"
    od['resource_type']    = resource_type
    od['id'] = id
    od['note'] = "This is only a stub for future implementation"
    
    return HttpResponse(json.dumps(od, indent=4),
                        content_type="application/json")
