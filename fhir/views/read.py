from django.shortcuts import render
from ..models import SupportedResourceType
from django.shortcuts import render
from collections import OrderedDict
from ..utils import (kickout_404, kickout_403)
from django.http import HttpResponse
import json

from django.conf import settings

def read(request, resource_type, id):
    """Read FHIR Interaction"""
    # Example client use in curl:
    # curl  -X GET http://127.0.0.1:8000/fhir/Practitioner/1234
    
    try:
        rt = SupportedResourceType.objects.get(resource_name=resource_type)
        if rt.access_denied(access_to_check="fhir_read"):
            msg = "%s access denied to %s records on this FHIR server." % ("READ",
                                                                           resource_type)
            return kickout_403(msg)


    except SupportedResourceType.DoesNotExist:
        msg = "%s is not a supported resource type on this FHIR server." % (resource_type)
        return kickout_404(msg)
    


    od = OrderedDict()
    od['request_method']= request.method
    od['interaction_type'] = "read"
    od['resource_type']    = resource_type
    od['id'] = id
    od['note'] = "This is only a stub for future implementation"
    return HttpResponse(json.dumps(od, indent=4),
                        content_type="application/json")
