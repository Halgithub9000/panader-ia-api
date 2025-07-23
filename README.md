# Panader-IA API

API para la gestión de productos y pedidos de una panadería, desarrollada con FastAPI y SQLAlchemy.

## Características

- Listado de productos
- Creación de pedidos
- Gestión de relaciones entre productos y pedidos

## Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/Halgithub9000/panader-ia-api.git
   cd panader-ia-api
   ```
2. Crea y activa un entorno virtual:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Configuración

Crea un archivo `.env` en la raíz del proyecto con la configuración de tu base de datos PostgreSQL:

```
DB_HOST=tu_host
DB_PORT=5432
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
DB_NAME=tu_base_de_datos
```

## Ejecución

Inicia el servidor de desarrollo:

```bash
uvicorn app.main:app --reload
```

La API estará disponible en `http://127.0.0.1:8000`.

La documentación interactiva está en `http://127.0.0.1:8000/docs`.

## Endpoints principales

- `GET /productos`: Lista todos los productos
- `POST /pedido`: Crea un nuevo pedido

## Notas

- Las tablas se crean automáticamente al iniciar la app (solo para desarrollo).
- Para producción, usa migraciones con Alembic.

## Requisitos

- Python 3.8+
- PostgreSQL

## Licencia

MIT
