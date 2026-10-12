-- =====================================================================
-- CONJUNTO DE TRABAJO — Variante 3: Estacionalidad y ritmo de la operación
-- Tablas foco: rental, payment. Resultado: una fila por día con
-- cantidad de alquileres, ingresos y clientes activos.
--
-- SEGURO contra inyección:
--   1) cada nombre se valida contra el catálogo (sys.columns);
--   2) se inserta con QUOTENAME: SQL Server lo trata como nombre, nunca como código;
--   3) las fechas viajan como parámetros de sp_executesql, nunca en el texto.
--
-- Decisiones:
--   * COUNT(DISTINCT id_alquiler): si un alquiler tuviera más de un pago, el
--     LEFT JOIN repetiría la fila y COUNT simple inflaría la cantidad.
--   * Rango de fechas [fecha_inicio, fecha_fin] inclusivo: se compara contra
--     el día siguiente a fecha_fin, porque la columna guarda fecha y hora.
--   * Los ingresos se imputan a la fecha del alquiler (en esta base la fecha
--     de pago coincide con la del alquiler en el 100% de los casos).
-- =====================================================================
SET NOCOUNT ON;

-- 1. PARÁMETROS (los completa Python mediante params) -----------------
DECLARE @esquema          sysname  = :esquema;
DECLARE @t_alquiler       sysname  = :t_alquiler;          -- rental
DECLARE @t_pago           sysname  = :t_pago;              -- payment
DECLARE @c_id_alquiler    sysname  = :c_id_alquiler;       -- rental.rental_id
DECLARE @c_fecha          sysname  = :c_fecha_alquiler;    -- rental.rental_date
DECLARE @c_id_cliente     sysname  = :c_id_cliente;        -- rental.customer_id
DECLARE @c_pago_alquiler  sysname  = :c_pago_id_alquiler;  -- payment.rental_id
DECLARE @c_monto          sysname  = :c_monto;             -- payment.amount
DECLARE @fecha_inicio     date     = :fecha_inicio;
DECLARE @fecha_fin        date     = :fecha_fin;

-- 2. VALIDACIÓN: las 5 columnas deben existir en sus tablas ------------
IF (SELECT COUNT(*)
    FROM sys.columns c
    JOIN sys.tables  t ON t.object_id = c.object_id
    JOIN sys.schemas s ON s.schema_id = t.schema_id
    WHERE s.name = @esquema
      AND (   (t.name = @t_alquiler AND c.name IN (@c_id_alquiler, @c_fecha, @c_id_cliente))
           OR (t.name = @t_pago     AND c.name IN (@c_pago_alquiler, @c_monto)))
   ) <> 5
    THROW 50001, 'esquema.py no coincide con la base - tabla o columna inexistente.', 1;

-- 3. CONSULTA: nombres con QUOTENAME, fechas como parámetros -----------
DECLARE @sql nvarchar(max) = N'
SELECT
    CAST(a.' + QUOTENAME(@c_fecha) + N' AS DATE)        AS fecha,
    COUNT(DISTINCT a.' + QUOTENAME(@c_id_alquiler) + N') AS cantidad_alquileres,
    COALESCE(SUM(p.' + QUOTENAME(@c_monto) + N'), 0.0)   AS ingresos_totales,
    COUNT(DISTINCT a.' + QUOTENAME(@c_id_cliente) + N')  AS clientes_activos
FROM ' + QUOTENAME(@esquema) + N'.' + QUOTENAME(@t_alquiler) + N' AS a
LEFT JOIN ' + QUOTENAME(@esquema) + N'.' + QUOTENAME(@t_pago) + N' AS p     -- conserva alquileres sin pago
    ON a.' + QUOTENAME(@c_id_alquiler) + N' = p.' + QUOTENAME(@c_pago_alquiler) + N'
WHERE a.' + QUOTENAME(@c_fecha) + N' >= @fecha_inicio
  AND a.' + QUOTENAME(@c_fecha) + N' <  DATEADD(DAY, 1, @fecha_fin)
GROUP BY CAST(a.' + QUOTENAME(@c_fecha) + N' AS DATE)
ORDER BY fecha;';

EXEC sp_executesql @sql,
     N'@fecha_inicio date, @fecha_fin date',
     @fecha_inicio = @fecha_inicio,
     @fecha_fin    = @fecha_fin;

