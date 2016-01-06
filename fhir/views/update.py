from django.shortcuts import render
from collections import OrderedDict
from django.http import HttpResponse
from ..utils import kickout_404
import json
from django.views.decorators.csrf import csrf_exempt
from ..models import SupportedResourceType

@csrf_exempt
def update(request, resource_type, id):
    """Update FHIR Interaction"""
    # Example client use in curl:
    # curl -X PUT -H "Content-Type: application/json" --data @test.json http://127.0.0.1:8000/fhir/Practitioner/12345
    
    try:
        rt = SupportedResourceType.objects.get(resource_name=resource_type)    
    except SupportedResourceType.DoesNotExist:
        msg = "%s is not a supported resource type on this FHIR server." % (resource_type)
        return kickout_404(msg)
    
    od = OrderedDict()
    od['request_method']= request.method
    od['interaction_type'] = "update"
    od['resource_type']    = resource_type
    od['id'] = id
    od['note'] = "This is only a stub for future implementation"
    return HttpResponse(json.dumps(od, indent=4),
                        content_type="application/json")