from rest_framework import serializers

from places import models as places_models

class FormfactorSerializer(serializers.ModelSerializer):
    outside_volume = serializers.ReadOnlyField()
    inside_volume = serializers.ReadOnlyField()

    class Meta:
        model = places_models.Formfactor
        fields = '__all__'
        #read_only_fields = ('outside_volume', 'inside_volume')

