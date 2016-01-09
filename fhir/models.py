from django.db import models

# Create your models here.
# See link below for porting advice for Python 2 to 3
# https://docs.djangoproject.com/en/1.9/topics/python3/


from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class SupportedResourceType(models.Model):
    resource_name           = models.CharField(max_length=256, unique=True,
                                               db_index=True)
    json_schema             = models.TextField(max_length=5120, default="{}",
                                        help_text="{} indicates no schema.")
    fhir_get                = models.BooleanField(default=True, verbose_name="GET")
    fhir_put                = models.BooleanField(default=False, verbose_name="PUT")
    fhir_create             = models.BooleanField(default=False, verbose_name="Create")
    fhir_read               = models.BooleanField(default=True, verbose_name="Read")
    fhir_update             = models.BooleanField(default=False, verbose_name="Update")
    fhir_delete             = models.BooleanField(default=False, verbose_name="DELETE")
    fhir_search             = models.BooleanField(default=True, verbose_name="Search")
    fhir_history            = models.BooleanField(default=False, verbose_name="_history")

    # Python2 uses __unicode__(self):

    def __str__(self):
        return self.resource_name

    def access_denied(self, access_to_check="fhir_get"):
        if access_to_check.lower() == "fhir_get":
            return not self.fhir_get
        elif access_to_check.lower() == "fhir_put":
            return not self.fhir_put
        elif access_to_check.lower() == "fhir_create":
            return not self.fhir_create
        elif access_to_check.lower() == "fhir_read":
            return not self.fhir_read
        elif access_to_check.lower() == "fhir_update":
            return not self.fhir_update
        elif access_to_check.lower() == "fhir_delete":
            return not self.fhir_delete
        elif access_to_check.lower() == "fhir_search":
            return not self.fhir_search
        elif access_to_check.lower() == "fhir_history":
            return not self.fhir_history
        else:
            return True

    def access_permitted(self, access_to_check="fhir_get"):
        if access_to_check.lower() == "fhir_get":
            return self.fhir_get
        elif access_to_check.lower() == "fhir_put":
            return self.fhir_put
        elif access_to_check.lower() == "fhir_create":
            return self.fhir_create
        elif access_to_check.lower() == "fhir_read":
            return self.fhir_read
        elif access_to_check.lower() == "fhir_update":
            return self.fhir_update
        elif access_to_check.lower() == "fhir_delete":
            return self.fhir_delete
        elif access_to_check.lower() == "fhir_search":
            return self.fhir_search
        elif access_to_check.lower() == "fhir_history":
            return self.fhir_history
        else:
            return False
