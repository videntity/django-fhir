
from oauth2_provider.decorators import protected_resource
from django.views.decorators.http import require_POST
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .create import create
from .update import update
from .read import read

#@require_POST
@login_required()
#@protected_resource(scopes=["read write_consent"])
def oauth_create(request, resource_type):
    if request.method == "POST":
        return create(request, resource_type)
    return HttpResponse(status=501)


@login_required
def oauth_update(request, resource_type, id):
    if request.method == "PUT":
        return update(request, resource_type)
    elif request.method == "GET":
        return read(request, resource_type, id)
    if settings.DEBUG:
        print("fhir/oauth2/update: Passed protected_resource check:", request, resource_type, id)
    return HttpResponse(status=501)

@protected_resource()
def oauth_view(request, resource_type):
    if request.method == "GET":
        return read(request, resource_type)
    return HttpResponse(status=501)