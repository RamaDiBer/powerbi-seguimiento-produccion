"""
Synthetic data for the "Seguimiento de Producción" Power BI report.

Builds an Excel workbook with the same shape the Power Query reads:
  * Excel table "SLANOVEDADES" (one row per device and its timestamps per stage)
  * sheet "PRODUCCION" (operator name in column A, system user in column B)
Every value is invented: clients, serials, users and operator names.

Usage:
    python generate_demo_data.py
Then point the RutaExcel parameter in Power BI to seguimiento_produccion_demo.xlsx.
"""
import random
from datetime import date, datetime, time, timedelta

from openpyxl import Workbook
from openpyxl.worksheet.table import Table, TableStyleInfo

random.seed(42)

START, END = date(2026, 6, 1), date(2026, 11, 10)
DEVICES_PER_WORKDAY = (35, 75)

CLIENTS = [("Cliente Retail", 0.55), ("Operador Móvil", 0.25), ("Trade-in Online", 0.12), ("Particular", 0.08)]
MODELS = {
    "SAMSUNG": ["GALAXY A15 128 GB", "GALAXY A25 128 GB", "GALAXY A35 256 GB", "GALAXY A55 256 GB",
                "GALAXY S23 128 GB", "GALAXY S24 256 GB", "GALAXY Z FLIP5 256 GB"],
    "MOTOROLA": ["MOTO G54 128 GB", "MOTO G84 256 GB", "EDGE 40 256 GB"],
    "APPLE": ["IPHONE 12 128 GB", "IPHONE 13 128 GB", "IPHONE 14 256 GB"],
    "XIAOMI": ["REDMI NOTE 13 128 GB", "REDMI 13C 128 GB"],
}
BRAND_W = {"SAMSUNG": 0.7, "MOTOROLA": 0.15, "APPLE": 0.1, "XIAOMI": 0.05}
OPERATORS = [("Lucía Fernández", "OP01"), ("Martín Sosa", "OP02"), ("Carla Giménez", "OP03"),
             ("Diego Romero", "OP04"), ("Valentina Ruiz", "OP05"), ("Nicolás Acosta", "OP06"),
             ("Julieta Medina", "OP07"), ("Tomás Herrera", "OP08"), ("Sofía Castro", "OP09")]
STAGE_USERS = {  # who usually works each stage
    "RECEPCIONADO": ["OP01", "OP02"], "GRADE COMPRA": ["OP03", "OP04"], "COSMETICO": ["OP04", "OP05"],
    "FUNCIONAL": ["OP06", "OP07"], "BATERIA": ["OP07", "OP08"], "DISPOSICION FINAL": ["OP08", "OP09"],
}
SALE_GRADES = [("A", 0.04), ("B", 0.12), ("C", 0.28), ("D", 0.30), ("E", 0.14), ("SLV", 0.12)]
BATTERY = [("Superior a 95%", 0.12), ("Entre 91% y 95%", 0.14), ("Entre 85% y 89,9%", 0.10),
           ("Entre 81% y 90%", 0.10), ("Inferior a 80%", 0.04), ("Ok", 0.12), ("Sin dato", 0.38)]

HEADERS = ["ID", "HANDSET_QUOTE_ID", "SERIAL_NUMBER", "PROYECTO", "MARCA", "MODELO", "LOTE", "FECHA_CREACION",
           "ETAPA_PROCESO", "Grading MPX", "Grading de Compra", "Grading de Venta", "BATERÍA",
           "FECHA PRE-RECEPCION", "USR PRE-RECEPCION", "FECHA RECEPCIONADO", "USR RECEPCIONADO",
           "FECHA GRADE COMPRA", "USR GRADE COMPRA", "FECHA COSMETICO", "USR COSMETICO",
           "FECHA FUNCIONAL", "USR FUNCIONAL", "FECHA BATERIA", "USR BATERIA",
           "FECHA DISPOSICION FINAL", "USR DISPOSICION FINAL", "FECHA DESPACHO", "FECHA CIERRE",
           "FECHA ENVIO A REPARO", "FECHA_DEVOLUCION_DE_REPARO"]


def pick(weighted):
    items, weights = zip(*weighted)
    return random.choices(items, weights=weights)[0]


def workday_after(d, days):
    d = d + timedelta(days=days)
    while d.weekday() >= 5:
        d += timedelta(days=1)
    return d


def shift_time(d, after=None):
    """Random timestamp inside the 06:00-15:00 shift, never before `after`."""
    t = datetime.combine(d, time(6)) + timedelta(minutes=random.randint(0, 540))
    if after and t <= after:
        t = after + timedelta(minutes=random.randint(5, 90))
    return t


def main(path="seguimiento_produccion_demo.xlsx"):
    now = datetime.combine(END, time(13, 19))
    rows, next_id = [], 1_000_001
    d = START
    while d <= END:
        if d.weekday() < 5:
            for _ in range(random.randint(*DEVICES_PER_WORKDAY)):
                brand = pick(list(BRAND_W.items()))
                created = shift_time(d)
                row = dict.fromkeys(HEADERS)
                row.update({
                    "ID": next_id, "HANDSET_QUOTE_ID": f"Q-{random.randint(100000, 999999)}",
                    "SERIAL_NUMBER": f"DEMO{next_id:08d}", "PROYECTO": pick(CLIENTS), "MARCA": brand,
                    "MODELO": random.choice(MODELS[brand]), "LOTE": f"L-{d:%y%m}-{random.randint(1, 12):02d}",
                    "FECHA_CREACION": created, "Grading MPX": random.choice(["1", "2", "3", "4"]),
                })
                next_id += 1
                if random.random() < 0.03:
                    row["ETAPA_PROCESO"] = "CANCELADO"
                    rows.append(row)
                    continue
                t = created
                # pre-reception and reception (some devices are still in transit)
                pre = workday_after(d, random.randint(0, 2))
                if pre > END:
                    row["ETAPA_PROCESO"] = "PENDIENTE"
                    rows.append(row)
                    continue
                t = shift_time(pre, t)
                row["FECHA PRE-RECEPCION"], row["USR PRE-RECEPCION"] = t, "OP01"
                stages = ["RECEPCIONADO", "GRADE COMPRA", "COSMETICO", "FUNCIONAL", "BATERIA", "DISPOSICION FINAL"]
                last = "PRE-RECEPCION"
                for stage in stages:
                    gap = random.choices([0, 1, 2, 3, 6, 12], weights=[45, 25, 12, 8, 6, 4])[0]
                    day = workday_after(t.date(), gap)
                    if day > END or (day == END and random.random() < 0.5):
                        break
                    t = shift_time(day, t)
                    key = "FECHA GRADE COMPRA" if stage == "GRADE COMPRA" else f"FECHA {stage}"
                    row[key] = t
                    row[f"USR {stage}"] = random.choice(STAGE_USERS[stage])
                    last = stage
                    if stage == "GRADE COMPRA":
                        row["Grading de Compra"] = random.choice(["1", "1", "4", "4", "9"])
                    if stage == "FUNCIONAL" and random.random() < 0.06:
                        row["FECHA ENVIO A REPARO"] = t + timedelta(hours=2)
                        back = workday_after(t.date(), random.randint(3, 15))
                        if back > END:
                            break
                        row["FECHA_DEVOLUCION_DE_REPARO"] = shift_time(back)
                        t = row["FECHA_DEVOLUCION_DE_REPARO"]
                    if stage == "BATERIA":
                        row["BATERÍA"] = pick(BATTERY)
                    if stage == "DISPOSICION FINAL":
                        row["Grading de Venta"] = pick(SALE_GRADES)
                        ship = workday_after(t.date(), random.randint(1, 10))
                        if ship <= END:
                            row["FECHA DESPACHO"] = shift_time(ship, t)
                            row["FECHA CIERRE"] = row["FECHA DESPACHO"] + timedelta(hours=1)
                row["ETAPA_PROCESO"] = last
                rows.append(row)
        d += timedelta(days=1)

    wb = Workbook()
    ws = wb.active
    ws.title = "BASE"
    ws.append(HEADERS)
    for r in rows:
        ws.append([r[h] for h in HEADERS])
    for col in ws.iter_cols(min_row=2):
        if isinstance(col[0].value, datetime) or "FECHA" in str(ws.cell(1, col[0].column).value):
            for c in col:
                c.number_format = "dd/mm/yyyy hh:mm"
    table = Table(displayName="SLANOVEDADES", ref=f"A1:{ws.cell(1, len(HEADERS)).column_letter}{len(rows) + 1}")
    table.tableStyleInfo = TableStyleInfo(name="TableStyleMedium2", showRowStripes=True)
    ws.add_table(table)

    prod = wb.create_sheet("PRODUCCION")
    prod.append(["OPERARIO", "USUARIO"])
    for name, user in OPERATORS:
        prod.append([name, user])

    wb.save(path)
    print(f"Wrote {len(rows)} fake devices to {path} (data until {now:%d/%m/%Y})")


if __name__ == "__main__":
    main()
