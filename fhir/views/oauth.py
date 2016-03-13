from oauth2_provider.decorators import protected_resource
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from .create import create
from .update import update
from .delete import delete
from .read import read



@require_POST
@protected_resource()
def oauth_create(request, resource_type):
    return create(request, resource_type)

@protected_resource()
def oauth_update(request, resource_type, id):
    if request.method == "PUT":
        return update(request, resource_type)
    return HttpResponse(status=501)

#@protected_resource()
def oauth_read_or_update_or_delete(request, resource_type, id):
    """Route to read, update, or delete based on HTTP method FHIR Interaction"""
     
    if request.method == 'GET':
        # Read
        return read(request, resource_type, id)
    elif request.method == 'PUT':
        # update
        return update(request, resource_type, id)
    elif request.method == 'DELETE':
        # delete
        return delete(request, resource_type, id)
    #else:
    # Not supported.
    msg = "HTTP method %s not supported at this URL." % (request.method)
    return kickout_400(msg)









