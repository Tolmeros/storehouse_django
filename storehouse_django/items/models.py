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
    humanid = models.CharField(max_length=50) # Поставить уникальный

    place = models.ForeignKey(
        StoragePlace,
        unique=False,
        related_name="items",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return "humanid='%s',comment='%s'" % (self.humanid, self.comment)
