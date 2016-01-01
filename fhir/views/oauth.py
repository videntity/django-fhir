from oauth2_provider.decorators import protected_resource
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from .create import create
from .update import update

@require_POST
@protected_resource()
def oauth_create(request, resource_type):
    return create(request, resource_type)

@protected_resource()
def oauth_update(request, resource_type):
    if request.method == "PUT":
        return update(request, resource_type)
    return HttpResponse(status=501)