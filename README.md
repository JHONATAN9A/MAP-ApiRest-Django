# Proyecto API Municipios Colombia

API REST para consultar municipios por departamento y obtener el municipio al que pertenece una oficina, con soporte de autenticación JWT.

---

## Tecnologías

- Python 3.x  
- Django  
- Django REST Framework  
- Django REST Framework Simple JWT  
- GeoDjango para datos geográficos  

---

## Variables de configuración

Antes de ejecutar el proyecto, debes configurar las siguientes variables (por ejemplo en un archivo `.env` o directamente en `settings.py`):

```
NAME_DB=""
USER_DB=""
PASSWORD_DB=""
HOST_DB=""
PORT_DB=""

SECRET_KEY=""
DEBUG=True
```

- **NAME_DB**: nombre de la base de datos  
- **USER_DB**: usuario de la base de datos  
- **PASSWORD_DB**: contraseña de la base de datos  
- **HOST_DB**: host de la base de datos (ej. localhost)  
- **PORT_DB**: puerto de la base de datos (ej. 5432 para PostgreSQL)  
- **SECRET_KEY**: clave secreta de Django para seguridad  
- **DEBUG**: activar/desactivar modo debug (usar False en producción)  

---

## Instalación y despliegue local

1. **Clonar el repositorio**

```
git clone <url-del-repositorio>
cd <nombre-del-proyecto>
```

2. **Crear y activar entorno virtual**

```
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. **Instalar dependencias**

```
pip install -r requirements.txt
```

4. **Configurar base de datos y migraciones**

Configura tu base de datos en `settings.py` (recomendado PostgreSQL con PostGIS para soporte geográfico).

```
python manage.py migrate
```

5. **Ejecutar servidor local**

```
python manage.py runserver
```

---

## Endpoints disponibles

| URL                      | Método | Descripción                                  | Parámetros Query                          |
|--------------------------|--------|----------------------------------------------|------------------------------------------|
| `/api/token/`             | POST   | Obtener token JWT (access y refresh)         | `username`, `password` (en body JSON)    |
| `/api/token/refresh/`     | POST   | Refrescar token JWT                           | `refresh` (en body JSON)                  |
| `/municipios/`            | GET    | Obtener municipios por departamento          | `departamento` (nombre del departamento) |
| `/municipio-por-oficina/` | GET    | Obtener municipio que contiene una oficina   | `id` (gid de la oficina)                  |

---

## Autenticación

Los endpoints `/municipios/` y `/municipio-por-oficina/` requieren token JWT en el header `Authorization`:

```
Authorization: Bearer <access_token>
```

---

## Ejemplos de uso

### Obtener token JWT

```
curl -X POST http://localhost:8000/api/token/ \
 -H "Content-Type: application/json" \
 -d '{"username":"tu_usuario","password":"tu_contraseña"}'
```

Respuesta:

```json
{
  "refresh": "<refresh_token>",
  "access": "<access_token>"
}
```

### Obtener municipios por departamento

```
curl -X GET "http://localhost:8000/municipios/?departamento=Antioquia" \
 -H "Authorization: Bearer <access_token>"
```

Respuesta ejemplo:

```json
[
  {
    "id": 1,
    "codigo_dane": "05001",
    "departamento": "Antioquia",
    "municipio": "Medellín",
    "disposicion": "urbano",
    "año_creacion": "1616"
  }
]
```

### Obtener municipio por oficina

```
curl -X GET "http://localhost:8000/municipio-por-oficina/?id=10" \
 -H "Authorization: Bearer <access_token>"
```

Respuesta ejemplo (GeoJSON simplificado):

```json
{
  "id": 5,
  "codigo_dane": "05010",
  "departamento": "Antioquia",
  "municipio": "Bello",
  "disposicion": "urbano",
  "año_creacion": "1813",
  "geometry": {
    "type": "Polygon",
    "coordinates": [...]
  }
}
```

---

## Notas

- Asegúrate de configurar correctamente las variables de entorno y `settings.py` para la conexión y seguridad.  
- El proyecto usa GeoDjango, por lo que requiere instalación y configuración previa de librerías geoespaciales (PostGIS, GDAL, GEOS).  
