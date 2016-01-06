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

    # Python2 uses __unicode__(self):

    def __str__(self):
        return self.resource_name