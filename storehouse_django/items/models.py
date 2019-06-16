from django.db import models
from places.models import StoragePlace

class ItemsBaseModel(models.Model):
    comment = models.CharField(
        default='',
        max_length=255,
        blank=True,
    )

    class Meta:
        abstract=True

class Item(ItemsBaseModel):
    humanid = models.CharField(
        max_length=50,
        unique=True,
        blank=True,
        null=True,
    )

    place = models.ForeignKey(
        StoragePlace,
        unique=False,
        related_name="items",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    def __str__(self):
        return "humanid='%s',comment='%s'" % (self.humanid, self.comment)
