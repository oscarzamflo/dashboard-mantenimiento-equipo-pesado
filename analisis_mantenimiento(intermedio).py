"""
Análisis Exploratorio - Dashboard de Mantenimiento de Equipo Pesado
--------------------------------------------------------------------
Proyecto de portafolio con datos simulados.
Calcula KPIs de costo, tiempo de reparación y tasa de reincidencia,
agrupados por tipo de servicio, sector de cliente y técnico responsable,
además de la tendencia mensual de costos.
"""

import pandas as pd

# 1. Carga de datos ----------------------------------------------------------
df = pd.read_csv("hpk_mantenimiento_dataset.csv", parse_dates=["Fecha"])
df["Mes"] = df["Fecha"].dt.to_period("M")

print(f"Órdenes totales: {len(df)}")
print(f"Rango de fechas: {df['Fecha'].min().date()} a {df['Fecha'].max().date()}")

# 2. KPIs generales ------------------------------------------------------------
kpi_generales = {
    "Costo Total (PEN)": df["Costo_Total_PEN"].sum(),
    "N° Órdenes": len(df),
    "Tiempo Promedio Reparación (hrs)": df["Tiempo_Reparacion_Horas"].mean(),
    "Tasa de Reincidencia (%)": (df["Reincidencia"] == "Sí").mean() * 100,
}
print("\n=== KPIs Generales ===")
for k, v in kpi_generales.items():
    print(f"{k}: {v:,.2f}")

# 3. Agrupación por Tipo de Servicio -------------------------------------------
kpis_por_servicio = df.groupby("Tipo_Servicio").agg(
    Costo_Total=("Costo_Total_PEN", "sum"),
    Costo_Promedio=("Costo_Total_PEN", "mean"),
    Tiempo_Promedio_hrs=("Tiempo_Reparacion_Horas", "mean"),
    N_Ordenes=("Orden_ID", "count"),
    Tasa_Reincidencia_pct=("Reincidencia", lambda s: (s == "Sí").mean() * 100),
).round(2).sort_values("Costo_Total", ascending=False)

print("\n=== KPIs por Tipo de Servicio ===")
print(kpis_por_servicio)

# 4. Agrupación por Sector de Cliente -------------------------------------------
kpis_por_sector = df.groupby("Sector_Cliente").agg(
    Costo_Total=("Costo_Total_PEN", "sum"),
    N_Ordenes=("Orden_ID", "count"),
    Tiempo_Promedio_hrs=("Tiempo_Reparacion_Horas", "mean"),
    Tasa_Reincidencia_pct=("Reincidencia", lambda s: (s == "Sí").mean() * 100),
).round(2).sort_values("Costo_Total", ascending=False)

print("\n=== KPIs por Sector de Cliente ===")
print(kpis_por_sector)

# 5. Agrupación por Técnico Responsable ------------------------------------------
kpis_por_tecnico = df.groupby("Tecnico_Responsable").agg(
    N_Ordenes=("Orden_ID", "count"),
    Costo_Promedio=("Costo_Total_PEN", "mean"),
    Tiempo_Promedio_hrs=("Tiempo_Reparacion_Horas", "mean"),
    Tasa_Reincidencia_pct=("Reincidencia", lambda s: (s == "Sí").mean() * 100),
).round(2).sort_values("N_Ordenes", ascending=False)

print("\n=== KPIs por Técnico Responsable ===")
print(kpis_por_tecnico)

# 6. Matriz cruzada: Sector vs. Tipo de Servicio (costo total) -------------------
matriz_sector_servicio = df.groupby(["Sector_Cliente", "Tipo_Servicio"])["Costo_Total_PEN"] \
    .sum().unstack(fill_value=0).round(2)
matriz_sector_servicio["Total"] = matriz_sector_servicio.sum(axis=1)
matriz_sector_servicio.loc["Total"] = matriz_sector_servicio.sum()

print("\n=== Matriz Costo Total: Sector de Cliente x Tipo de Servicio ===")
print(matriz_sector_servicio)

# 7. Tendencia mensual de costo total ---------------------------------------------
tendencia_mensual = df.groupby("Mes")["Costo_Total_PEN"].sum().round(2)

print("\n=== Tendencia Mensual de Costo Total ===")
print(tendencia_mensual)

# 8. Exportar resultados a Excel (una hoja por tabla) para usarlos en Power BI -----
with pd.ExcelWriter("resultados_analisis_mantenimiento.xlsx") as writer:
    kpis_por_servicio.to_excel(writer, sheet_name="KPIs_Tipo_Servicio")
    kpis_por_sector.to_excel(writer, sheet_name="KPIs_Sector_Cliente")
    kpis_por_tecnico.to_excel(writer, sheet_name="KPIs_Tecnico")
    matriz_sector_servicio.to_excel(writer, sheet_name="Matriz_Sector_Servicio")
    tendencia_mensual.to_excel(writer, sheet_name="Tendencia_Mensual")

print("\nResultados exportados a 'resultados_analisis_mantenimiento.xlsx'")
