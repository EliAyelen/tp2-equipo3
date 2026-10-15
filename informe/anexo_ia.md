# Anexo de Trazabilidad de IA

## 0. Herramientas y método de trabajo
A lo largo del trabajo se utilizaron cuatro herramientas de IA, cada una con un rol
definido. ChatGPT funcionó como traductor de prompts: se le pasaba el contexto con
nuestras propias palabras y lo convertía en un prompt para otra herramienta. NotebookLM
actuó como tutor, acotado a nuestra bibliografía (diapositivas y apunte de la Unidad 5,
consigna del TP2, informe del TP1 y repositorio del docente). Gemini se usó como
corrector de código e ideas durante la construcción de las Actividades 1 a 3, mientras
el código se iba armando. Por último, Claude, se incorporó como auditor técnico en la
Actividad 3, con el trabajo ya armado; a partir de su auditoría se revisaron las
Actividades 0 a 3. 

Por otro lado, el repositorio del docente fue una referencia constante: se lo utilizó
como esqueleto de base para entender los ejemplos, replicarlos sobre nuestra base y
comparar nuestras soluciones con las propuestas de la cátedra.

No se registraron casos en que una herramienta inventara nombres de tablas o columnas:
todos los nombres se validaron contra esquema.py y, del lado del motor, contra
sys.columns.

## 1. Bitácora de prompts

### ChatGPT — Ingeniero de prompts
> Actuá como nuestro ingeniero de prompts para el Trabajo Práctico 2 del Seminario de
> Actualización (Equipo 3, Variante 3: Estacionalidad y ritmo de la operación, sobre la
> base Sakila migrada a SQL Server). De ahora en más, te vamos a pasar contexto tal como
> lo hablamos entre nosotros, con nuestro léxico y sin un orden fijo, y vos lo vas a
> traducir en un prompt robusto para otra IA. Antes de redactar cada prompt, preguntanos
> todo lo que te falte: qué IA lo va a recibir, qué rol tiene que asumir, a qué actividad
> del TP corresponde, con qué fuentes cuenta y qué tipo de respuesta esperamos. No
> completes datos que no te dimos ni agregues requisitos que no mencionamos. Cada prompt
> tiene que incluir el rol, el contexto, el objetivo, las restricciones (la consigna del
> TP2 y la bibliografía de la Unidad 5 son norma; no inventar nombres de tablas ni de
> columnas; explicar el porqué en lugar de resolvernos el trabajo) y el formato de
> respuesta. Devolvé solamente el prompt, listo para copiar.

### NotebookLM — Tutor
> **Rol:** Actúa como nuestro Consultor y Tutor de Ingeniería y Analítica de Datos (Data
> Engineering & Analytics Tutor) para el desarrollo del Trabajo Práctico 2 (Variante 3:
> Estacionalidad y ritmo de la operación).
> **Contexto y Fuentes:** Tu conocimiento debe acotarse estrictamente a los documentos
> cargados en este notebook (diapositivas de la Unidad 5, consigna del TP2, informe y
> conclusiones del TP1, apunte de cátedra y repositorio del docente).
> **Objetivo:** Guianos metodológica y conceptualmente en la resolución de los puntos que
> consultemos. No buscamos que avances en un código resuelto a ciegas, sino que actúes como
> un mentor técnico: explicando el "porqué" de las buenas prácticas de la Unidad 5
> (pushdown a SQL Server, parametrización, vectorización en Pandas, manejo riguroso de
> series temporales).

**Corrección:** propuso completar los días sin registros con fillna(0) y sostuvo que
agrupar por DATE no eliminaba información; ambas inferencias se corrigieron (léase
sección 3).

### Gemini — Corrector de código e ideas
> Actuá como nuestro Corrector y Tutor de Data Engineering / Data Analytics (nivel
> Senior).
> Te pongo en contexto: Somos el Equipo 3 de la materia "Seminario de Actualización"
> (TP2 sobre Sakila, Variante 3: Estacionalidad y ritmo de la operación). Necesitamos que
> seas nuestro consultor técnico y guía de aprendizaje.
> Específicamente, necesitamos tu revisión y feedback sobre los siguientes aspectos clave:
> 1. Revisión de Consultas SQL y Agregaciones Iniciales:
>    - Evaluá la consulta T-SQL que construye nuestro conjunto de trabajo sobre 'alquiler'
>      (rental) y 'pago' (payment).
> 2. Eliminación de f-strings (Pauta Estricta Unidad 5):
>    - Auditá nuestro código de carga en Pandas para asegurar que no estemos usando
>      concatenación de cadenas ni f-strings dentro de las consultas SQL.
>    - Orientanos sobre cómo implementar correctamente la parametrización de filtros
>      (:fecha_inicio, :fecha_fin) mediante la clase text() de SQLAlchemy y pd.read_sql,
>      evitando fallas de seguridad o malas prácticas.
> 3. Análisis de Métricas Diarias y Duda sobre "Comprimir" Información:
>    - Explicanos desde el punto de vista conceptual y del negocio: Sabiendo que en una
>      misma fecha existen múltiples alquileres individuales, ¿por qué no estamos
>      perdiendo registros al agrupar por DATE?
> 4. Perfilado y Detección Temprana de Inconsistencias:
>    - Revisá nuestros primeros scripts de perfilado y diagnósticos en Python (shape,
>      info, describe, duplicados y reglas de negocio).
> Adoptá un tono didáctico pero exigente (como un Ingeniero de Datos Senior),
> indicándonos qué hacemos bien, qué debemos corregir según el apunte de la Unidad 5.

**Corrección:** la v2 de la extracción que propuso era segura, pero dejaba el nombre
de la tabla escrito fuera de esquema.py, por lo que no era portable.

### Claude — Auditor técnico
> Actuá como auditor técnico del Trabajo Práctico 2 del Seminario de Actualización
> (Equipo 3, Variante 3: Estacionalidad y ritmo de la operación). Trabajamos sobre
> nuestra base Sakila migrada a SQL Server (esquema sakila, nombres en español), con
> Python, pandas, SQLAlchemy y pyodbc, y tomamos como referencia el repositorio del
> docente. Te vamos a pasar la consigna completa, que es norma estricta, junto con
> nuestro código y el notebook de las Actividades 0 a 3. Verificá, paso por paso, si
> cumplimos cada punto y si caemos en alguna de las condiciones que por sí solas impiden
> aprobar. Ante cada problema, explicá por qué lo es, citando la consigna o la Unidad 5,
> y proponé la corrección. No afirmes nada que no puedas sostener con nuestro código o
> con las salidas del notebook; si te falta información, preguntá.

**Corrección:** propuso un cuarto hallazgo que atribuía el índice más bajo del martes a
la cobertura horaria de los martes de cierre; el equipo lo descartó por no estar
suficientemente sostenido. 

## 2. Crítica de código: cómo llegan los nombres de tablas y columnas a las consultas
La extracción de los datos crudos de la Actividad 1.4, que la consigna exige resolver
íntegramente en pandas, pasó por tres versiones generadas con IA, que fuimos adaptando
sobre el esqueleto del repositorio del docente y sobre lo que ya teníamos construido.

**v1 (NotebookLM):** `text(f"SELECT id_alquiler, fecha_alquiler, id_cliente FROM {TABLAS['rental']}")`,
surgida de un ejemplo propuesto por NotebookLM. Su punto a favor es la simpleza y que
lee los nombres desde el diccionario. Sin embargo, arma la consulta concatenando texto
con una f-string, práctica que la consigna considera un error grave.

**v2 (Gemini):** `read_sql_table(table_name="alquiler", schema=ESQUEMA, columns=["id_alquiler", …])`.
Lejos de concatenar, delega la construcción de la consulta en SQLAlchemy, de manera segura. Su único problema es que el nombre "alquiler" y los de las columnas quedaron escritos fuera de esquema.py, rompiendo la portabilidad.

**v3 (Claude):** se resolvió en dos partes. En la extracción de la 1.4 se mantuvo
read_sql_table, pero los nombres se obtienen de esquema.py:
`read_sql_table(table_name=obtener_tabla("rental"), schema=ESQUEMA, columns=[obtener_columna("rental", "rental_id"), …])`.
En conjunto_trabajo.sql, en cambio, los nombres viajan como parámetros, se validan
contra sys.columns y se insertan con QUOTENAME, y las fechas se pasan por
sp_executesql. Si bien esta última utiliza SQL dinámico, lo hace de forma controlada,
dado que los nombres de tablas y columnas no pueden pasarse como parámetros comunes. Su
costo es una consulta más extensa y menos legible.

**Nuestra versión:** la versión final no es ninguna de las tres tal cual. Como bien se
mencionó, el repositorio del docente fue nuestro esqueleto: de allí tomamos la
estructura del módulo de conexión, con la lectura de variables de entorno y la
autenticación integrada, y la organización del pipeline en extraer, transformar y
cargar. Sin embargo, el repositorio no resolvía la portabilidad de los nombres, por lo
que sobre la v3 integramos nuestro esquema.py y la consulta que ya resolvía la unión
entre alquiler y pago y la agregación diaria. La v3 hace mejor la seguridad y la
portabilidad.

## 3. Conclusión analítica no sostenida por los datos
Al construir la serie sobre el calendario completo, NotebookLM propuso completar los
días sin registros con fillna(0). Detrás de esa línea había una conclusión implícita:
que en esos días la tienda estuvo cerrada o no hubo alquileres. Los datos no sostienen
esa afirmación; lo único que puede afirmarse es que no hay registros. El problema se
terminó de confirmar en la auditoría de Claude de la Actividad 3 y lo revalidamos al ver que los
ceros hacían caer la media móvil. Por ello, los huecos quedaron como NaN y la media
móvil pasó a exigir al menos 4 días reales en la ventana (min_periods=4).

Dentro de este marco, existió una segunda inferencia de NotebookLM: que agrupar por DATE no eliminaba información. Si bien es cierto que no perdimos registros (la suma diaria da los 
16.044 alquileres), sí se pierde la hora de cada uno, que tuvimos que revisar aparte y que fue justamente la que terminó explicando el comportamiento de los martes.

Respecto a de qué días excluir, en un primer momento excluimos solo los dos extremos del período, el 24/05/2005 y el 14/02/2006 (39 días de base). Al buscar los huecos, contrastamos las fechas con un calendario real de 2005 y 2006 y vimos que cada bloque abría y cerraba un martes, con 8
días exactos de datos y brechas de 13. A partir de ahí revisamos la base con consultas
propias por hora y encontramos que los martes de apertura solo tenían actividad desde
las 22:50 aproximadamente (cerca de una hora) y que el 14/02/2006 concentraba 182
alquileres a las 15:16:03. Por lo tanto, excluimos del índice los 5 martes de apertura
y el 14/02/2006, y la base quedó en 35 días, 5 por cada día de la semana.
