"""
URL configuration for prueba_tecnica project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.urls import path
from django.contrib import admin
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from api.views import *
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),  # Panel de administración de Django
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Obtener token JWT
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refrescar token JWT
    path('municipios/', MunicipiosPorDepartamentoView.as_view(), name='municipios_por_departamento'),  # Municipios por departamento
    path('municipio-por-oficina/', MunicipioPorOficinaView.as_view(), name='municipio-por-oficina'),  # Municipio según oficina (geolocalización)
]


handler403 = 'prueba_tecnica.views.custom_403'
handler404 = 'prueba_tecnica.views.custom_404'
handler500 = 'prueba_tecnica.views.custom_500'