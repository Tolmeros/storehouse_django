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
    
    humanid = models.CharField(max_length=5, unique=False) 

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

    @property
    def full_humanid(self):
        return '%s%03d%s' % (self.opening_type.humanid,
                             self.formfactor.humanid, self.humanid)
    # Сделать что бы можно было писать и оно раскладывало на 
    # opening_type, formfactor и humanid
    

    def __str__(self):
        return "full_humanid='%s',humanid='%s', comment='%s'" % (
            self.full_humanid,
            self.humanid,
            self.comment
        )

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

    @property
    def outside_volume(self):
        if self.outside_height and self.outside_width and self.outside_depth:
            return self.outside_height * self.outside_width * self.outside_depth

    @property
    def inside_volume(self):
        if self.inside_height and self.inside_width and self.inside_depth:
            return self.inside_height * self.inside_width * self.inside_depth

    def __str__(self):
        return "humanid=%d,comment='%s'" % (self.humanid, self.comment)


class OpeningType(PlacesBaseModel):
    
    humanid = models.CharField(max_length=1, unique=True) # Поставить уникальный
    
    def __str__(self):
        return "humanid='%s',comment='%s'" % (self.humanid, self.comment)
