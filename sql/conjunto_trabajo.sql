-- Variante 3: Estacionalidad Y ritmo de la operacion
-- Consulta sobre tabla foco (alquileres y pagos) para un analisis con fechas 

SELECT 
    CAST(a.fecha_alquiler AS DATE) AS fecha,
    COUNT(a.id_alquiler) AS cantidad_alquileres,
    COALESCE(SUM(p.monto), 0.0) AS ingresos_totales,
    COUNT(DISTINCT a.id_cliente) AS clientes_activos
FROM  [sakila].[alquiler] a
LEFT JOIN [sakila].[pago] p 
    ON a.id_alquiler = p.id_alquiler
WHERE a.fecha_alquiler >= :fecha_inicio 
  AND a.fecha_alquiler <= :fecha_fin
GROUP BY CAST(a.fecha_alquiler AS DATE)
ORDER BY fecha ASC;
