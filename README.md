# 🏭 Seguimiento de producción

![Power BI](https://img.shields.io/badge/Power%20BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)
![DAX](https://img.shields.io/badge/DAX-1557b0?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Formato](https://img.shields.io/badge/formato-.pbip-555?style=for-the-badge)

> Dashboard operativo para una línea de **reacondicionamiento de equipos**: cuántas unidades pasan por cada etapa, cómo vamos contra el plan, qué tan productivo es cada operario y cuánto trabajo queda en proceso.

## 📌 Qué responde

- ¿Cuántas unidades se procesaron hoy, en el mes y en el acumulado?
- ¿Estamos cumpliendo el **objetivo** y el **plan**?
- ¿Cuántas unidades por hora y por operario-día se producen?
- ¿Qué porcentaje termina como **ABC** y cuánto como **scrap**?
- ¿Cuánto tarda un equipo en recorrer el proceso (**lead time**) y cuánto **WIP** hay en planta?

## 🔄 Etapas del proceso

`Recepción → Compra → Cosmética → Funcional → Batería → Disposición final (ABC / Scrap)`

## 🧱 Modelo de datos

| Tabla | Contenido |
|---|---|
| `Equipos` | Una fila por equipo con su recorrido por las etapas |
| `Eventos` | Movimientos de cada equipo entre etapas |
| `Etapas` | Catálogo y orden de etapas |
| `Operarios` / `NombresOperarios` | Personal de la línea |
| `Horas` | Horas trabajadas |
| `Calendario` / `Periodos` | Dimensión de fechas y selector de período |
| `Medidas` | 50+ medidas DAX |

La fuente es un Excel diario de producción, leído desde el parámetro `RutaExcel`.

## 📐 Medidas principales

| Grupo | Medidas |
|---|---|
| Volumen | Unidades, Uds por etapa, Unidades acumuladas, Promedio diario |
| Cumplimiento | Objetivo, Plan, % Cumplimiento objetivo/plan, Diferencia vs objetivo |
| Productividad | Operarios activos, Horas activas, Unidades por hora, Unidades por operario-día |
| Calidad | % ABC, % Scrap |
| Flujo | Lead time mediano, En planta, En reparo, Pendientes de recepción, Antigüedad promedio WIP |
| Formato | Medidas `Color …` y `Txt …` para formato condicional y textos dinámicos |

## 📄 Páginas del informe

1. **Resumen** — KPIs principales y cumplimiento del plan
2. **Operarios** — productividad por persona
3. **Calidad y grading** — resultados de disposición final
4. **Producción del día** — foto diaria por etapa
5. **Flujo y WIP** — stock en proceso y antigüedad
6. **Detalle de equipos** — trazabilidad individual

## ▶️ Cómo abrirlo

1. Abrir `Seguimiento de Produccion.pbip` con Power BI Desktop.
2. En **Transformar datos → Parámetros**, apuntar `RutaExcel` al Excel de producción.
3. Actualizar.

> 🔒 Los datos de producción contienen información del personal, por lo que el repositorio incluye solo el modelo, las medidas y el diseño del informe, sin datos.
