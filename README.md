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


