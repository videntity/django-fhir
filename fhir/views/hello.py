from django.shortcuts import render
from ..models import SupportedResourceType
from collections import OrderedDict
from django.http import HttpResponse

import json, uuid

def hello(request):
    """Hello FHIR"""
    # Example client use in curl:
    # curl http://127.0.0.1:8000/fhir/hello
    res_types = SupportedResourceType.objects.all()    
    rnames = []
    for r in res_types:
        rnames.append(r.resource_name)
  
    #This is something other than POST (i.e. a  GET)
    od = OrderedDict()
    od['request_method']= request.method
    od['supported_resource_types']    = rnames
    od['supported_interaction_types'] = ["create", "read",
                                         "update", "delete",
                                         "search"]
    od['note'] = "Hello.  Welcome to the FHIR Server."
    return HttpResponse(json.dumps(od, indent=4),
                        content_type="application/json")