from rest_framework import serializers

from places import models as places_models
from items import models as items_models

class FormfactorSerializer(serializers.ModelSerializer):
    outside_volume = serializers.ReadOnlyField()
    inside_volume = serializers.ReadOnlyField()

    class Meta:
        model = places_models.Formfactor
        fields = '__all__'
        #read_only_fields = ('outside_volume', 'inside_volume')


class OpeningTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = places_models.OpeningType
        fields = '__all__'

class StoragePlaceSerializer(serializers.ModelSerializer):
    full_humanid = serializers.ReadOnlyField()
    #place = serializers.PrimaryKeyRelatedField(queryset=places_models.StoragePlace.objects.all())
    #inside_places = serializers.PrimaryKeyRelatedField(queryset=places_models.StoragePlace.objects.all())

    class Meta:
        #depth = 1
        model = places_models.StoragePlace
        fields = '__all__'

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = items_models.Item
        fields = '__all__'


class ItemTypeSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = items_models.ItemType
        fields = '__all__'


