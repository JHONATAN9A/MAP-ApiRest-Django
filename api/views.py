from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import *
from .serializers import *

class MunicipiosPorDepartamentoView(APIView):
    """
    Devuelve los municipios de un departamento dado.

    Requiere autenticación y el parámetro de consulta `departamento`.

    Respuestas:
    - 200: Lista de municipios.
    - 400: Falta el parámetro.
    - 404: Departamento sin municipios.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        nombre_departamento = request.query_params.get('departamento')
        if not nombre_departamento:
            return Response({'error': 'Debe proporcionar el parámetro "departamento"'}, status=400)

        municipios = MunicipiosColombiaModel.objects.filter(departamento__iexact=nombre_departamento)
        if not municipios.exists():
            return Response({'error': f'No se encontraron municipios para el departamento "{nombre_departamento}"'}, status=404)

        serializer = MunicipioSerializer(municipios, many=True)
        return Response(serializer.data, status=200)


class MunicipioPorOficinaView(APIView):
    """
    Devuelve el municipio al que pertenece una oficina, usando su geometría.

    Requiere autenticación y el parámetro de consulta `id` (gid de la oficina).

    Respuestas:
    - 200: Municipio en formato GeoJSON.
    - 400: Falta el parámetro.
    - 404: Oficina o municipio no encontrado.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        oficina_id = request.query_params.get('id')
        if not oficina_id:
            return Response({'error': 'Debe proporcionar el parámetro id'}, status=400)

        try:
            oficina = PuntosOficinasModel.objects.get(gid=oficina_id)
        except PuntosOficinasModel.DoesNotExist:
            return Response({'error': 'Oficina no encontrada'}, status=status.HTTP_404_NOT_FOUND)

        municipio_example = MunicipiosColombiaModel.objects.first()
        if not municipio_example:
            return Response({'error': 'No hay municipios cargados'}, status=status.HTTP_404_NOT_FOUND)

        punto_transformado = oficina.geometry.transform(municipio_example.geometry.srid, clone=True)

        try:
            municipio = MunicipiosColombiaModel.objects.get(geometry__contains=punto_transformado)
        except MunicipiosColombiaModel.DoesNotExist:
            return Response({'error': 'Municipio no encontrado para la oficina'}, status=status.HTTP_404_NOT_FOUND)

        if municipio.geometry:
            municipio.geometry = municipio.geometry.simplify(tolerance=0.001, preserve_topology=True)

        serializer = MunicipioGeoJsonSerializer(municipio)
        return Response(serializer.data)