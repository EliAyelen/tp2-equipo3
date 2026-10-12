-- =====================================================================
-- RECONCILIACIÓN — Actividad 0
-- Cuenta las filas de TODAS las tablas del esquema recibido por parámetro. 
-- No contiene ningún nombre propio de la
-- base del equipo: los nombres salen del catálogo (sys.tables), y Python los
-- traduce a nombres canónicos con esquema.TABLAS. Así el mismo archivo
-- funciona contra la base de cualquier equipo.
-- =====================================================================
SET NOCOUNT ON;

DECLARE @esquema sysname = :esquema;

IF SCHEMA_ID(@esquema) IS NULL
    THROW 50002, 'El esquema indicado en esquema.py no existe en la base.', 1;

-- QUOTENAME protege cada nombre; los nombres provienen del propio catálogo.
DECLARE @sql nvarchar(max);

SELECT @sql = STRING_AGG(
           CAST(N'SELECT ' + QUOTENAME(t.name, '''') + N' AS tabla_bd, '
                + N'COUNT_BIG(*) AS filas_sql_server FROM '
                + QUOTENAME(s.name) + N'.' + QUOTENAME(t.name) AS nvarchar(max)),
           N' UNION ALL ')
       WITHIN GROUP (ORDER BY t.name)
FROM sys.tables  t
JOIN sys.schemas s ON s.schema_id = t.schema_id
WHERE s.name = @esquema;

SET @sql = @sql + N' ORDER BY tabla_bd;';

EXEC sp_executesql @sql;

/* =====================================================================
   CONTEO EN EL ORIGEN (MySQL / HeidiSQL, base sakila original).


USE sakila;

SELECT 'actor' AS tabla, COUNT(*) AS filas_origen FROM actor
UNION ALL SELECT 'address', COUNT(*) FROM address
UNION ALL SELECT 'category', COUNT(*) FROM category
UNION ALL SELECT 'city', COUNT(*) FROM city
UNION ALL SELECT 'country', COUNT(*) FROM country
UNION ALL SELECT 'customer', COUNT(*) FROM customer
UNION ALL SELECT 'film', COUNT(*) FROM film
UNION ALL SELECT 'film_actor', COUNT(*) FROM film_actor
UNION ALL SELECT 'film_category', COUNT(*) FROM film_category
UNION ALL SELECT 'film_text', COUNT(*) FROM film_text
UNION ALL SELECT 'inventory', COUNT(*) FROM inventory
UNION ALL SELECT 'language', COUNT(*) FROM language
UNION ALL SELECT 'payment', COUNT(*) FROM payment
UNION ALL SELECT 'rental', COUNT(*) FROM rental
UNION ALL SELECT 'staff', COUNT(*) FROM staff
UNION ALL SELECT 'store', COUNT(*) FROM store;
   ===================================================================== */
