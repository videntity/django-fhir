django-fhir
===========

This software is in the very begining phases now. It is not ready for prime time at all. That said, here is how to install it.

(working on compatibility with MongoDb and a pluggable backend 
eg. to use back-end HAPI-FHIR Server via API calls)

To install type the following in a shell:

    git clone https://github.com/videntity/django-fhir.git
    pip install ./django-fhir
    

Add "fhir" to your INSTALLED_APPS setting like this:

    INSTALLED_APPS = (
        ...
        'fhir',
    )

Include the direct URLconf in your project urls.py like this:

    url(r'^fhir/', include('fhir.urls')),


Create your database tables.


    python manage.py syncdb

Support a couple resource types by adding them in the admin or 
using the following command to activate `Practitioner` and `Organization`.


    python manage.py loaddata [your download path]/django-fhir/fhir/fixtures/provider-directory-resources.json


Use the APIs. Visit http://127.0.0.1:8000/fhir/hello to verify the installation.
  
# Pluggable backends
  
  Calls to a backend database for Django-fhir have been isolated to modules alongside the fhir
  module in djang-fhir. We are adopting the convention for naming these pluggable database
  backends as follows:
    fhir_io_{backend_name}
   
  The Default setting for django_fhir (in fhir.settings.py) can be overridden by adding 
  
  DJANGO_FHIR_CONFIG = {
    "DF_APPS": {'fhir_io_mongo',
                }
  }   

  to your applications settings.py. The only restriction is that the pluggable module must:
  1. Be added at the top level of your app. i.e. 'fhir_io_postgresql' works but 
    'apps.fhir_io_postgresql' won't load correctly.
  2. You must replicate the functions included in the reference fhir_io_mongo pluggable module
     complete with the parameters passed to each function.
     
  This architecture allows new database backends to be integrated into the django-fhir 
  architecture. 
  
   
# BlueButton On FHIR Support:

UPDATE: SupportedResourceType model has been extended to allow FHIR Transaction Types for a 
given resource to be permitted or denied. ie. Allow Patient resource to be searched but
update or Delete can be denied. Each FHIR Transaction mode is a BooleanField in the database.
SupportedResourceType.access_denied("field_name") or 
SupportedResourceType.access_permitted("field_name") will return a True or False value.

example usage:
    from .utils import check_access_interaction_and_resource_type

    interaction_type = 'read'
    #Check if this interaction type and resource type combo is allowed.
    deny = check_access_interaction_and_resource_type(resource_type, interaction_type)
    if deny:
        #If not allowed, return a 4xx error.
        return deny

