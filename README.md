README
======

This software is very begining phases now. Not ready for prime time.

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
usi the folloing command to activate `Practioner` and `Organization`.


    python manage.py loaddata [your download path]/django-fhir/fhir/fixtures/provider-directory-resources.json


Use the APIs. Visit http://127.0.0.1:8000/fhir/hello to verify 
the installation.
   
