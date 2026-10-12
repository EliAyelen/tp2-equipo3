"""Pipeline ETL — TP2, Variante 3: Estacionalidad y ritmo de la operación.
Extrae de SQL Server (alquiler y pago) y de un archivo plano,
transforma (limpieza, serie diaria, MM7 e índice de estacionalidad)
y carga en TP2_SerieDiariaOperacion."""

import logging
import sys
from pathlib import Path

import pandas as pd
from sqlalchemy import Integer, MetaData, Table, cast, distinct, func, select, text
from sqlalchemy.types import Boolean, Date, Float, NVARCHAR, Numeric

# Raíz del proyecto en el camino de búsqueda
RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from config_conexion import obtener_engine
from esquema import ESQUEMA, nombres_conjunto_trabajo

# Rutas armadas desde la ubicación del script
RUTA_SQL = RAIZ / "sql" / "conjunto_trabajo.sql"
RUTA_CSV = RAIZ / "pipeline" / "datos" / "clasificacion_dias.csv"

PARAMS = {"fecha_inicio": "2005-01-01", "fecha_fin": "2006-12-31"}

TABLA_DESTINO = "TP2_SerieDiariaOperacion"

DIAS_ES = {0: "Lunes", 1: "Martes", 2: "Miércoles", 3: "Jueves",
           4: "Viernes", 5: "Sábado", 6: "Domingo"}

# Tipo SQL Server de cada columna de la tabla destino 
TIPOS_DESTINO = {
    "fecha":                 Date(),           
    "dia_semana":            NVARCHAR(10),     
    "con_datos":             Boolean(),        
    "cantidad_alquileres":   Integer(),        
    "ingresos_totales":      Numeric(10, 2),   
    "clientes_activos":      Integer(),
    "alquileres_mm7":        Float(),          
    "ingresos_mm7":          Float(),
    "dias_con_datos_semana": Integer(),
    "excluido_indice":       Boolean(),
    "motivo_exclusion":      NVARCHAR(100),
    "indice_alquileres":     Float(),
    "indice_ingresos":       Float(),
}

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("pipeline_tp2")


def extraer(engine):
    log.info("Inicio: extraer")

    # Origen 1: SQL Server. Nombres reales desde esquema.py y fechas por params
    consulta = text(RUTA_SQL.read_text(encoding="utf-8"))
    parametros = {**nombres_conjunto_trabajo(), **PARAMS}
    diario = pd.read_sql(consulta, con=engine, params=parametros)
    log.info("SQL Server: %d filas leídas (días con datos)", len(diario))

    # Origen 2: archivo plano
    clasificacion = pd.read_csv(RUTA_CSV, sep=";", encoding="utf-8-sig")
    log.info("Archivo plano: %d filas leídas (días clasificados)", len(clasificacion))

    log.info("Fin: extraer")
    return diario, clasificacion


def transformar(diario, clasificacion):
    
    log.info("Inicio: transformar (%d días con datos)", len(diario))

    # 1. Tipado
    diario = diario.assign(fecha=pd.to_datetime(diario["fecha"], errors="coerce"))
    clasificacion = clasificacion.assign(fecha=pd.to_datetime(clasificacion["fecha"]))

    # 2. Controles: no se descartan filas 
    faltantes = int(diario.isna().sum().sum())
    duplicados = int(diario["fecha"].duplicated().sum())
    log.info("Controles Act 2: %d faltantes | %d fechas duplicadas", faltantes, duplicados)
    if faltantes or duplicados:
        log.warning("Aparecieron faltantes o duplicados que la Act 2 no registró: revisar el origen")

    # 3. Calendario completo (reindex): los huecos quedan como NaN, nunca como 0
    serie = diario.set_index("fecha").sort_index()
    calendario = pd.date_range(serie.index.min(), serie.index.max(), freq="D", name="fecha")
    serie = serie.reindex(calendario)
    serie["con_datos"] = serie["cantidad_alquileres"].notna()

    # 4. Merge con el archivo plano: marca los días que no entran al índice
    serie = (serie.reset_index()
             .merge(clasificacion, on="fecha", how="left", validate="one_to_one")
             .rename(columns={"motivo": "motivo_exclusion"})
             .set_index("fecha"))
    serie["excluido_indice"] = serie["tipo_dia"].notna()
    if serie["excluido_indice"].sum() != len(clasificacion):
        log.warning("Hay fechas del archivo plano que no están en el calendario")

    # 5. Media móvil de 7 días (rolling), igual que el notebook: solo en días con datos
    serie["alquileres_mm7"] = (serie["cantidad_alquileres"]
                               .rolling(window=7, min_periods=4).mean()
                               .where(serie["con_datos"]))
    serie["ingresos_mm7"] = (serie["ingresos_totales"]
                             .rolling(window=7, min_periods=4).mean()
                             .where(serie["con_datos"]))

    # 6. Resumen semanal (resample): días con datos en la semana de cada fecha
    serie["dias_con_datos_semana"] = serie["con_datos"].resample("W").transform("sum")

    # 7. Índice de estacionalidad
    serie["num_dia"] = serie.index.dayofweek
    base = serie[serie["con_datos"] & ~serie["excluido_indice"]]
    indice = base.groupby("num_dia").agg(
        alquileres_promedio=("cantidad_alquileres", "mean"),
        ingresos_promedio=("ingresos_totales", "mean"))
    indice["indice_alquileres"] = indice["alquileres_promedio"] / base["cantidad_alquileres"].mean()
    indice["indice_ingresos"] = indice["ingresos_promedio"] / base["ingresos_totales"].mean()
    log.info("Índice: base de %d días (%d excluidos según el archivo plano)",
             len(base), int(serie["excluido_indice"].sum()))

    serie = (serie.reset_index()
             .merge(indice[["indice_alquileres", "indice_ingresos"]],
                    left_on="num_dia", right_index=True, how="left"))
    serie["dia_semana"] = serie["num_dia"].map(DIAS_ES)

    # 8. Columnas de la tabla destino; conteos enteros que admiten NULL (Int64)
    serie = serie[["fecha", "dia_semana", "con_datos",
                   "cantidad_alquileres", "ingresos_totales", "clientes_activos",
                   "alquileres_mm7", "ingresos_mm7", "dias_con_datos_semana",
                   "excluido_indice", "motivo_exclusion",
                   "indice_alquileres", "indice_ingresos"]]
    serie = serie.astype({"cantidad_alquileres": "Int64", "clientes_activos": "Int64"})

    log.info("Fin: transformar (%d filas: %d con datos, %d sin datos)",
             len(serie), int(serie["con_datos"].sum()), int((~serie["con_datos"]).sum()))
    return serie


def cargar(engine, serie):
    """Reemplaza por completo la tabla destino, dentro de una única transacción."""
    log.info("Inicio: cargar (%d filas en %s.%s)", len(serie), ESQUEMA, TABLA_DESTINO)

    
    with engine.begin() as conexion:
        serie.to_sql(TABLA_DESTINO, con=conexion, schema=ESQUEMA,
                     if_exists="replace", index=False,
                     chunksize=1000, dtype=TIPOS_DESTINO)

    log.info("Fin: cargar (%d filas insertadas)", len(serie))


def verificar(engine, filas_esperadas):
    
    log.info("Inicio: verificar")

    tabla = Table(TABLA_DESTINO, MetaData(), schema=ESQUEMA, autoload_with=engine)
    consulta = select(
        func.count().label("filas"),
        func.count(distinct(tabla.c.fecha)).label("fechas_distintas"),
        func.sum(cast(tabla.c.con_datos, Integer)).label("dias_con_datos"),
        func.sum(tabla.c.cantidad_alquileres).label("alquileres"),
    )
    with engine.connect() as conexion:
        conteo = conexion.execute(consulta).one()

    log.info("Verificación %s.%s: filas=%d | fechas distintas=%d | "
             "días con datos=%d | alquileres=%d",
             ESQUEMA, TABLA_DESTINO, conteo.filas, conteo.fechas_distintas,
             conteo.dias_con_datos, conteo.alquileres)

    if conteo.filas != filas_esperadas or conteo.fechas_distintas != conteo.filas:
        raise RuntimeError("La tabla destino no coincide con lo transformado")
    log.info("Fin: verificar")


def ejecutar_pipeline():
    """Orquesta las etapas en orden. Un fallo se registra completo y se relanza."""
    log.info("=== Pipeline TP2 (Variante 3): inicio ===")
    try:
        engine = obtener_engine()
        diario, clasificacion = extraer(engine)
        serie = transformar(diario, clasificacion)
        cargar(engine, serie)
        verificar(engine, filas_esperadas=len(serie))
        log.info("=== Pipeline TP2: finalizado correctamente ===")
    except Exception:
        log.exception("El pipeline falló")
        raise


if __name__ == "__main__":
    ejecutar_pipeline()
