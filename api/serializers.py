from rest_framework import serializers
from .models import *

class MunicipioSerializer(serializers.ModelSerializer):
    """Serializa datos básicos del municipio."""
    class Meta:
        model = MunicipiosColombiaModel
        fields = ('id', 'codigo_dane', 'departamento', 'municipio', 'disposicion', 'año_creacion')


class MunicipioGeoJsonSerializer(serializers.ModelSerializer):
    """Serializa municipio con geometría (GeoJSON)."""
    class Meta:
        model = MunicipiosColombiaModel
        fields = ('id', 'codigo_dane', 'departamento', 'municipio', 'disposicion', 'año_creacion', 'geometry')