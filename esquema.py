"""Traduce los nombres canónicos de Sakila (en inglés) a los nombres exactos
de tablas y columnas elegidos en la migración de SQL Server (sakila_espanol)."""

# Mapeo de esquema 
ESQUEMA = "sakila"

# Mapeo de las 16 Tablas: Nombre canónico (inglés) -> Nombre en español
TABLAS = {
    "actor": f"{ESQUEMA}.actor",
    "address": f"{ESQUEMA}.direccion",
    "category": f"{ESQUEMA}.categoria",
    "city": f"{ESQUEMA}.ciudad",
    "country": f"{ESQUEMA}.pais",
    "customer": f"{ESQUEMA}.cliente",
    "film": f"{ESQUEMA}.pelicula",
    "film_actor": f"{ESQUEMA}.pelicula_actor",
    "film_category": f"{ESQUEMA}.pelicula_categoria",
    "film_text": f"{ESQUEMA}.pelicula_texto",
    "inventory": f"{ESQUEMA}.inventario",
    "language": f"{ESQUEMA}.idioma",
    "payment": f"{ESQUEMA}.pago",
    "rental": f"{ESQUEMA}.alquiler",
    "staff": f"{ESQUEMA}.empleado",
    "store": f"{ESQUEMA}.tienda",
}

# Mapeo de Columnas de las 16 Tablas
COLUMNAS = {
    "actor": {
        "actor_id": "id_actor",
        "first_name": "nombre",
        "last_name": "apellido",
        "last_update": "ultima_actualizacion",
    },
    "address": {
        "address_id": "id_direccion",
        "address": "direccion",
        "address2": "direccion2",
        "district": "distrito",
        "city_id": "id_ciudad",
        "postal_code": "codigo_postal",
        "phone": "telefono",
        "last_update": "ultima_actualizacion",
    },
    "category": {
        "category_id": "id_categoria",
        "name": "nombre",
        "last_update": "ultima_actualizacion",
    },
    "city": {
        "city_id": "id_ciudad",
        "city": "ciudad",
        "country_id": "id_pais",
        "last_update": "ultima_actualizacion",
    },
    "country": {
        "country_id": "id_pais",
        "country": "pais",
        "last_update": "ultima_actualizacion",
    },
    "customer": {
        "customer_id": "id_cliente",
        "store_id": "id_tienda",
        "first_name": "nombre",
        "last_name": "apellido",
        "email": "email",
        "address_id": "id_direccion",
        "active": "activo",
        "create_date": "fecha_creacion",
        "last_update": "ultima_actualizacion",
    },
    "film": {
        "film_id": "id_pelicula",
        "title": "titulo",
        "description": "descripcion",
        "release_year": "anio_estreno",
        "language_id": "id_idioma",
        "original_language_id": "id_idioma_original",
        "rental_duration": "duracion_alquiler",
        "rental_rate": "tarifa_alquiler",
        "length": "duracion",
        "replacement_cost": "costo_reemplazo",
        "rating": "clasificacion",
        "special_features": "caracteristicas_especiales",
        "last_update": "ultima_actualizacion",
    },
    "film_actor": {
        "actor_id": "id_actor",
        "film_id": "id_pelicula",
        "last_update": "ultima_actualizacion",
    },
    "film_category": {
        "film_id": "id_pelicula",
        "category_id": "id_categoria",
        "last_update": "ultima_actualizacion",
    },
    "film_text": {
        "film_id": "id_pelicula",
        "title": "titulo",
        "description": "descripcion",
    },
    "inventory": {
        "inventory_id": "id_inventario",
        "film_id": "id_pelicula",
        "store_id": "id_tienda",
        "last_update": "ultima_actualizacion",
    },
    "language": {
        "language_id": "id_idioma",
        "name": "nombre",
        "last_update": "ultima_actualizacion",
    },
    "payment": {
        "payment_id": "id_pago",
        "customer_id": "id_cliente",
        "staff_id": "id_empleado",
        "rental_id": "id_alquiler",
        "amount": "monto",
        "payment_date": "fecha_pago",
        "last_update": "ultima_actualizacion",
    },
    "rental": {
        "rental_id": "id_alquiler",
        "rental_date": "fecha_alquiler",
        "inventory_id": "id_inventario",
        "customer_id": "id_cliente",
        "return_date": "fecha_devolucion",
        "staff_id": "id_empleado",
        "last_update": "ultima_actualizacion",
    },
    "staff": {
        "staff_id": "id_empleado",
        "first_name": "nombre",
        "last_name": "apellido",
        "address_id": "id_direccion",
        "picture": "foto",
        "email": "email",
        "store_id": "id_tienda",
        "active": "activo",
        "username": "usuario",
        "password": "contrasenia",
        "last_update": "ultima_actualizacion",
    },
    "store": {
        "store_id": "id_tienda",
        "manager_staff_id": "id_empleado_gerente",
        "address_id": "id_direccion",
        "last_update": "ultima_actualizacion",
    },
}

# Funciones auxiliares de consulta de esquema

def obtener_tabla(tabla_canonica: str) -> str:
    """Retorna el nombre real de la tabla en la base de datos local."""
    return TABLAS.get(tabla_canonica, tabla_canonica)

def obtener_columna(tabla_canonica: str, columna_canonica: str) -> str:
    """Retorna el nombre real de una columna en la base de datos local."""
    return COLUMNAS.get(tabla_canonica, {}).get(columna_canonica, columna_canonica)

def obtener_mapping_columnas(tabla_canonica: str) -> dict:
    """
    Retorna el diccionario de mapeo completo (Inglés -> Español) para una tabla.
    """
    return COLUMNAS.get(tabla_canonica, {})

def obtener_mapping_inverso_columnas(tabla_canonica: str) -> dict:
    """
    Retorna el mapeo inverso (Español -> Inglés).
    Facilita renombrar las columnas que vienen de SQL Server hacia los DataFrames de pandas.
    """
    mapping_directo = COLUMNAS.get(tabla_canonica, {})
    return {v: k for k, v in mapping_directo.items()}

if __name__ == "__main__":
    print("\n==========================================")
    print(" VERIFICACIÓN DE ESQUEMA (16 Tablas)")
    print("==========================================")
    print(f"Total de tablas mapeadas: {len(TABLAS)}")
    print(f"Tabla 'rental' -> Base local: '{obtener_tabla('rental')}'")
    print(f"Tabla 'film_actor' -> Base local: '{obtener_tabla('film_actor')}'")
    print(f"Columna 'rental_date' -> '{obtener_columna('rental', 'rental_date')}'")
    print(f"Columna 'amount' -> '{obtener_columna('payment', 'amount')}'")
    print("==========================================\n")
