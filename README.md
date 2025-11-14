# First-api — Series App

Pequeña API REST con frontend estático para gestionar series (CRUD) con autenticación JWT.

## Estado
- Backend: Flask + Flask-JWT-Extended + SQLAlchemy
- Frontend: Vanilla JS, servido estático desde `frontend/`
- Tema UI: naranja/negro, tipografía Montserrat, botones con ripple y toast

## Requisitos
- Python 3.8+
- Dependencias en `requirements.txt` (instalar con `pip install -r requirements.txt`).

## Ejecución (desarrollo)

1. Iniciar backend (en la raíz del repo):

```powershell
$env:DEBUG='0'; python app.py
```

Con `DEBUG=1` el servidor usará autoreload; para pruebas E2E recomendamos `DEBUG=0`.

2. Servir frontend (opcional — para abrir en navegador):

```powershell
cd frontend
python -m http.server 5500
# abrir http://127.0.0.1:5500
```

3. Probar rutas manualmente o ejecutar pruebas E2E (desde la raíz):

```powershell
python -u tests\api_e2e.py
```

El E2E crea un usuario `e2e_admin` con contraseña `admin123` si no existe, hace login y prueba crear/editar/borrar una serie.

## Notas de diseño
- Tokens JWT: `identity` se guarda como string para evitar errores de algunas librerías.
- Frontend guarda `token`, `role` y `username` en `localStorage`.
- Se agregó UI mejorada en `frontend/styles.css` y microinteracciones en `frontend/app.js`.

## Archivos modificados principales
- `app.py`, `services/auth_service.py`
- `frontend/` (`index.html`, `api.js`, `app.js`, `auth.js`, `home.js`, `admin.js`, `styles.css`)
- `tests/api_e2e.py`

## Próximos pasos recomendados
- Usar servidor WSGI (Gunicorn/Waitress) y HTTPS para producción.
- Añadir manejo de refresh tokens o re-login automático en frontend.
- Mejorar validación de formularios y mensajes de error en UI.

---
Si quieres, hago el deploy en un contenedor o agrego CI para ejecutar tests.
# CRUD API REST de Series de Comedia

Este proyecto implementa una API REST en **Flask** para gestionar una
lista de series de comedia.\
Se desarrolló siguiendo buenas prácticas de organización de carpetas y
manejo de ramas en GitHub.

##  Funcionalidades

  Método   Endpoint                Descripción
  -------- ----------------------- ---------------------------
  GET      /series                 Obtiene todas las series.
  GET      /series/`<id>`{=html}   Obtiene una serie por ID.
  POST     /series                 Crea una nueva serie.
  PUT      /series/`<id>`{=html}   Actualiza una serie.
  DELETE   /series/`<id>`{=html}   Elimina una serie.

------------------------------------------------------------------------

##  Estructura del Proyecto

    First-api/
    ├── app.py                 # Punto de entrada de la aplicación
    ├── controllers/           # Controladores (manejan las rutas)
    │   └── series_controller.py
    ├── services/              # Lógica de negocio
    │   └── series_service.py
    ├── models/                # Datos simulados o modelos
    │   └── series_model.py
    └── venv/                  # Entorno virtual (ignorado en .gitignore)

------------------------------------------------------------------------

##  Ramas de Desarrollo

Durante el desarrollo se trabajó con ramas para mantener el flujo de
trabajo ordenado:

-   `main` → Rama principal\
-   `feature-stats` → Implementación de estadísticas dentro de la API.\
-   `feature-add-validation` → Validación de número mínimo de campos
    para ingresar el nombre de una serie.\
-   `feature-buscar-plataforma` → Desarrollo del endpoint de búsqueda de
    series por plataforma.

------------------------------------------------------------------------

##  Instalación y Ejecución

1.  **Clonar el repositorio:**

    ``` bash
    git clone https://github.com/diegojaramillov/First-api.git
    cd First-api
    ```

2.  **Crear y activar entorno virtual:**

    ``` bash
    python -m venv venv
    source venv/Scripts/activate   # (Git Bash en Windows)
    ```

3.  **Instalar dependencias:**

    ``` bash
    pip install flask
    ```

4.  **Ejecutar el servidor:**

    ``` bash
    python app.py
    ```

El servidor correrá en: `http://127.0.0.1:5000`

------------------------------------------------------------------------

##  Ejemplos de Prueba con CURL

**GET todas las series:**

``` bash
curl http://127.0.0.1:5000/series
```

**POST (crear serie):**

``` bash
curl -X POST -H "Content-Type: application/json" -d '{"name": "Friends", "seasons": 10}' http://127.0.0.1:5000/series
```

**PUT (actualizar serie):**

``` bash
curl -X PUT -H "Content-Type: application/json" -d '{"name": "Friends (Remastered)"}' http://127.0.0.1:5000/series/1
```

**DELETE (eliminar serie):**

``` bash
curl -X DELETE http://127.0.0.1:5000/series/1
```

## Autenticación y Autorización

El sistema implementa **JWT (JSON Web Tokens)** para la autenticación y autorización de usuarios.
Se manejan 2 roles principales:

* **admin** → Puede acceder a todas las rutas, crear, actualizar y eliminar recursos.
* **user** → Solo puede acceder a rutas públicas (ej: listar series).

---

###  Rutas de autenticación

#### **Registro**

```http
POST /auth/register
```

**Body (JSON):**

```json
{
  "username": "user1",
  "password": "user123",
  "role": "user"
}
```

#### **Login**

```http
POST /auth/login
```

**Body (JSON):**

```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Respuesta:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "user": {
    "id": 1,
    "username": "admin",
    "role": "admin"
  }
}
```

El valor de `access_token` debe incluirse en el header de las peticiones a rutas protegidas:

```
Authorization: Bearer <ACCESS_TOKEN>
```

---

###  Rutas de Series (ejemplo de validación por rol)

#### **Listar series (público)**

```http
GET /series/
```

#### **Crear serie (solo admin)**

```http
POST /series/
```

**Body (JSON):**

```json
{
  "title": "Breaking Bad",
  "description": "Serie sobre química y crimen",
  "year": 2008
}
```

#### **Actualizar serie (solo admin)**

```http
PUT /series/<id>
```

#### **Eliminar serie (solo admin)**

```http
DELETE /series/<id>
```

---

###  Validación de roles

* Los endpoints de administración (`POST`, `PUT`, `DELETE` en `/series`) requieren rol `admin`.
* Si un usuario con rol `user` intenta acceder, recibe:

```json
{
  "error": "Access forbidden: insufficient role"
}
```


