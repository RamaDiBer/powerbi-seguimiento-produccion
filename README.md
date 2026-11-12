# 🏭 Production Tracking

![Power BI](https://img.shields.io/badge/Power%20BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)
![DAX](https://img.shields.io/badge/DAX-1557b0?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Format](https://img.shields.io/badge/format-.pbip-555?style=for-the-badge)

> Operational dashboard for a **device refurbishing line**: how many units go through each stage, how we are doing against the plan, how productive each operator is and how much work is still in progress.

*The report itself (page names, measures, labels) is in Spanish.*

## 📌 Questions it answers

- How many units were processed today, this month and to date?
- Are we hitting the **target** and the **plan**?
- How many units per hour and per operator-day are produced?
- What share ends up as **ABC** (sellable) and how much as **scrap**?
- How long does a device take to go through the process (**lead time**), and how much **WIP** is on the floor?

## 🔄 Process stages

`Reception → Purchase grading → Cosmetic → Functional test → Battery test → Final disposition (ABC / Scrap)`

## 🧱 Data model

| Table | Content |
|---|---|
| `Equipos` | One row per device with its path through the stages |
| `Eventos` | Each device's moves between stages |
| `Etapas` | Stage catalog and order |
| `Operarios` / `NombresOperarios` | Line staff |
| `Horas` | Productive minutes per hourly slot |
| `Calendario` / `Periodos` | Date dimension and period selector |
| `Medidas` | 50+ DAX measures |

The source is a daily production Excel file, read from the `RutaExcel` parameter.

## 📐 Main measures

| Group | Measures |
|---|---|
| Volume | Units, units per stage, cumulative units, daily average |
| Attainment | Target, plan, % of target / plan, gap vs. target |
| Productivity | Active operators, active hours, units per hour, units per operator-day |
| Quality | % ABC, % scrap |
| Flow | Median lead time, on the floor, in repair, pending reception, average WIP age |
| Formatting | `Color …` and `Txt …` measures for conditional formatting and dynamic text |

## 📄 Report pages

1. **Resumen (Summary):** main KPIs and plan attainment
2. **Operarios (Operators):** productivity per person
3. **Calidad y grading (Quality):** final disposition results
4. **Producción del día (Today):** daily snapshot per stage
5. **Flujo y WIP (Flow):** work in progress and its age
6. **Detalle de equipos (Device detail):** per-device traceability

## ▶️ How to open it

1. Generate a synthetic dataset: `pip install openpyxl` and `python demo/generate_demo_data.py` (creates `seguimiento_produccion_demo.xlsx` with ~6,000 fake devices, operators and clients).
2. Open `Seguimiento de Produccion.pbip` in Power BI Desktop.
3. Under **Transform data → Parameters**, point `RutaExcel` to that file (or to the real production Excel).
4. Refresh.

> 🔒 Production data includes staff information, so the repository holds only the model, the measures and the report design, with no data.
