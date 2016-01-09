django-fhir
===========

This software is very begining phases now. Not ready for prime time.

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


Use the APIs. Visit http://127.0.0.1:8000/fhir/hello to verify 
the installation.
   
UPDATE: SupportedResourceType model has been extended to allow FHIR Transaction Types for a 
given resource to be permitted or denied. ie. Allow Patient resource to be searched but
update or Delete can be denied. Each FHIR Transaction mode is a BooleanField in the database.
SupportedResourceType.access_denied("field_name") or 
SupportedResourceType.access_permitted("field_name") will return a True or False value

example usage:

        try:
        rt = SupportedResourceType.objects.get(resource_name=resource_type)
        if rt.access_denied(access_to_check="fhir_delete"):
            msg = "%s access denied to %s records on this FHIR server." % ("DELETE",
                                                                           resource_type)
            return kickout_403(msg)
