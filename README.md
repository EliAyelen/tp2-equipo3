# TP2 — Del dato al análisis: Data Analytics e Ingeniería de Datos sobre Sakila

**Seminario de Actualización 2026 — Unidad 5**
Instituto Superior Nuestra Señora de Luján del Buen Viaje
Docente: Jorge Insfran

**Equipo 3 — Variante 3: Estacionalidad y ritmo de la operación**
Integrantes: Agustin De Boeuf, Eliana Gimenez, Melissa Herrera 

Análisis de la demanda diaria de alquileres e ingresos sobre la base Sakila migrada a SQL Server en el TP1, y pipeline ETL que carga la serie diaria en la tabla `sakila.TP2_SerieDiariaOperacion`.

## Requisitos
- Windows con PowerShell.
- Python 3.14 (versión con la que se probó el proyecto).
- SQL Server con la base `sakila` migrada.
- ODBC Driver 17 for SQL Server.

## Estructura
```
tp2-equipo3/
├── README.md
├── requirements.txt
├── .env.example              plantilla de variables de entorno
├── config_conexion.py        conexión, sin credenciales
├── esquema.py                nombres canónicos de Sakila -> nombres de nuestra base
├── sql/
│   ├── reconciliacion.sql
│   └── conjunto_trabajo.sql
├── notebooks/
│   └── analisis.ipynb        actividades 0 a 3, ejecutado
├── pipeline/
│   ├── pipeline_tp2.py       actividad 4
│   └── datos/clasificacion_dias.csv
├── graficos/                 PNG a 150 dpi
└── informe/
    ├── informe.pdf
    ├── diagnostico_calidad.pdf
    └── anexo_ia.md
```

## Ejecución paso a paso

1. Clona el repositorio y entra en la carpeta:

   git clone https://github.com/EliAyelen/tp2-equipo3.git
   cd tp2-equipo3

2. Crea y activa el entorno virtual:

   py -m venv venv_tp2
   .\venv_tp2\Scripts\Activate.ps1

   Si PowerShell bloquea la activación, ejecuta antes:
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

3. Instala las dependencias:

   python -m pip install -r requirements.txt

4. Crea el archivo de configuración local a partir de la plantilla:

   Copy-Item .env.example .env

   Edita `.env` y completa:

   DB_SERVER=<servidor\instancia>
   DB_NAME=<nombre_de_la_base>
   DB_DRIVER=ODBC Driver 17 for SQL Server
   DB_TRUSTED_CONNECTION=yes

   La conexión usa autenticación integrada de Windows, por lo que no hace falta usuario ni contraseña.

5. Verifica la conexión:

   python config_conexion.py

   Si todo está bien, se muestra "¡CONEXIÓN EXITOSA A SQL SERVER!" junto con el nombre
   de la base; si no, se muestra el error.

6. Ejecuta el análisis: inicia Jupyter desde la carpeta `notebooks`, abre
   `analisis.ipynb` y ejecuta las celdas en orden.

   Set-Location notebooks
   jupyter lab analisis.ipynb

7. Ejecuta el pipeline ETL desde la raíz del proyecto y consulta el código de salida:

   Set-Location ..
   python pipeline/pipeline_tp2.py
   $LASTEXITCODE

   `0` indica que el pipeline terminó correctamente; un valor distinto de `0` (por
   ejemplo `1`) indica que falló, y el detalle queda en el log. El pipeline reemplaza
   la tabla `sakila.TP2_SerieDiariaOperacion` en cada ejecución.

8. Verifica la idempotencia: ejecuta el paso 7 dos veces seguidas y corre en SQL
   Server la siguiente consulta. Después de cada ejecución el resultado debe ser el
   mismo: 267 filas, 267 fechas distintas, 41 días con datos y 16.044 alquileres.

   SELECT COUNT(*)                         AS filas,
          COUNT(DISTINCT fecha)            AS fechas_distintas,
          SUM(CAST(con_datos AS int))      AS dias_con_datos,
          SUM(cantidad_alquileres)         AS alquileres
   FROM sakila.TP2_SerieDiariaOperacion;

## Ejecutar sobre la base de otro equipo
Editar solamente `esquema.py`: los nombres de las tablas y columnas en `TABLAS` y
`COLUMNAS`, y el esquema en `ESQUEMA`. El resto del código usa los nombres canónicos de Sakila. En el `.env`, apuntar `DB_NAME` (y `DB_SERVER` si cambia) a la base de ese equipo.