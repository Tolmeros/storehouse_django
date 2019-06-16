from django.db import models

# Create your models here.

class PlacesBaseModel(models.Model):
    comment = models.CharField(
        default='',
        max_length=255,
        blank=True,
    )

    class Meta:
        abstract=True

class StoragePlace(PlacesBaseModel):
    
    humanid = models.CharField(max_length=5, unique=True) 

    place = models.ForeignKey(
        'self',
        unique=False,
        related_name="inside_places",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )


    formfactor = models.ForeignKey(
        'Formfactor',
        unique=False,
        related_name="storage_places",
        on_delete=models.CASCADE,
    )

    opening_type = models.ForeignKey(
        'OpeningType',
        unique=False,
        related_name="storage_places",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return "humanid='%s', comment='%s'" % (self.humanid, self.comment)

class Formfactor(PlacesBaseModel):

    humanid = models.IntegerField(unique=True) # Поставить уникальный

    outside_height =  models.IntegerField(blank=True, null=True)
    outside_width =  models.IntegerField(blank=True, null=True)
    outside_depth =  models.IntegerField(blank=True, null=True)
    inside_height =  models.IntegerField(blank=True, null=True)
    inside_width =  models.IntegerField(blank=True, null=True)
    inside_depth =  models.IntegerField(blank=True, null=True)
    empty_weight =  models.IntegerField(blank=True, null=True)
    contents_weight_max =  models.IntegerField(blank=True, null=True)

    def __str__(self):
        return "humanid='%d',comment='%s'" % (self.humanid, self.comment)


class OpeningType(PlacesBaseModel):
    
    humanid = models.CharField(max_length=1, unique=True) # Поставить уникальный
    
    def __str__(self):
        return "humanid='%s',comment='%s'" % (self.humanid, self.comment)
