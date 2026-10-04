-- Descripción:
--   Consulta T-SQL que contabiliza el número total de registros por cada una
--   de las 16 tablas pertenecientes al esquema 'sakila_espanol'.
-- ============================================================================

USE sakila_espanol; 
GO

SELECT 'actor' AS tabla, COUNT(*) AS filas_sql_server FROM [sakila].[actor]
UNION ALL SELECT 'alquiler', COUNT(*) FROM [sakila].[alquiler]
UNION ALL SELECT 'categoria', COUNT(*) FROM [sakila].[categoria]
UNION ALL SELECT 'ciudad', COUNT(*) FROM [sakila].[ciudad]
UNION ALL SELECT 'cliente', COUNT(*) FROM [sakila].[cliente]
UNION ALL SELECT 'direccion', COUNT(*) FROM [sakila].[direccion]
UNION ALL SELECT 'empleado', COUNT(*) FROM [sakila].[empleado]
UNION ALL SELECT 'idioma', COUNT(*) FROM [sakila].[idioma]
UNION ALL SELECT 'inventario', COUNT(*) FROM [sakila].[inventario]
UNION ALL SELECT 'pago', COUNT(*) FROM [sakila].[pago]
UNION ALL SELECT 'pais', COUNT(*) FROM [sakila].[pais]
UNION ALL SELECT 'pelicula', COUNT(*) FROM [sakila].[pelicula]
UNION ALL SELECT 'pelicula_actor', COUNT(*) FROM [sakila].[pelicula_actor]
UNION ALL SELECT 'pelicula_categoria', COUNT(*) FROM [sakila].[pelicula_categoria]
UNION ALL SELECT 'pelicula_texto', COUNT(*) FROM [sakila].[pelicula_texto]
UNION ALL SELECT 'tienda', COUNT(*) FROM [sakila].[tienda];

-- ============================================================================
-- Descripción:
--   Consulta comentada de MySQL que contabiliza el número total de registros por cada una
--   de las 16 tablas pertenecientes al esquema 'sakila'.
-- ============================================================================

"""
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

"""