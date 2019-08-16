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


class ItemType(ItemsBaseModel):
    
    name = models.CharField(
        max_length=250,
        unique=True,
        blank=True,
        null=True,
    )

    tsubtype = models.CharField(
        max_length=250,
        blank=True,
        null=True,
    )
    
    def __str__(self):
        return "name='%s',comment='%s'" % (self.name, self.comment)

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

    itemtype = models.ForeignKey(
        'ItemType',
        unique=False,
        related_name="items",
        on_delete=models.CASCADE,
        # Временно
        blank=True,
        null=True,
    )

    count = models.IntegerField(default=1)

    def __str__(self):
        return "humanid='%s',comment='%s',count=%d" % (
            self.humanid,
            self.comment,
            self.count
        )
