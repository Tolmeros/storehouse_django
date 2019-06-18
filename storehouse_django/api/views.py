#from django.shortcuts import render

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated

from . import serializers
#from places import models as places_models

# Create your views here.

class FormfactorViewSet(viewsets.ModelViewSet):
    __basic_fields = ('humanid', )
    serializer_class = serializers.FormfactorSerializer
    queryset = serializers.places_models.Formfactor.objects.all()
    permission_classes = (IsAuthenticated,)
    #filter_backends = (DjangoFilterBackend,)
    #filterset_fields = ('humanid', )
    #filter_fields = ('humanid', )
    #search_fields = ('humanid', )
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = __basic_fields
    search_fields = __basic_fields

