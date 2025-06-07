from django.db import models
from django.contrib.gis.db import models

class MunicipiosColombiaModel(models.Model):
    """Modelo de municipios con geometría (SRID 3116)."""
    codigo_dane = models.CharField(max_length=20)
    departamento = models.CharField(max_length=100)
    municipio = models.CharField(max_length=100)
    disposicion = models.CharField(max_length=100)
    año_creacion = models.CharField(max_length=10)
    geometry = models.GeometryField(srid=3116)

    class Meta:
        db_table = 'municipios_colombia'

    def __str__(self):
        return f"{self.municipio} ({self.departamento})"


class PuntosOficinasModel(models.Model):
    """Modelo de oficinas con punto geográfico (SRID 4326)."""
    gid = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    departamento = models.CharField(max_length=100)
    municipio = models.CharField(max_length=100)
    geometry = models.PointField(srid=4326)

    class Meta:
        db_table = 'puntos_oficinas'

    def __str__(self):
        return self.nombre