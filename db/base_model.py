from django.db import models


class BaseModel(models.Model):

    create_time = models.DateTimeField(auto_now_add=True, verbose_name="Create time")
    update_time = models.DateTimeField(auto_now=True, verbose_name="Updata time")
    is_delete = models.BooleanField(default=False, verbose_name="Confirm delete")
    
    # abstract model
    class Meta:
        abstract = True
