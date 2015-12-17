from django.db import models

# Create your models here.



class SupportedResourceType(models.Model):
    resource_name           = models.CharField(max_length=256, unique=True,
                                               db_index=True)
    json_schema             = models.TextField(max_length=5120, default="{}",
                                        help_text="{} indicates no schema.")

    def __unicode__(self):
        return self.resource_name