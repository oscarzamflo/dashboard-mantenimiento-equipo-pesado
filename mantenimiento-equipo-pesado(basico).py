import pandas as pd

df = pd.read_csv("hpk_mantenimiento_dataset.csv")

print (df.head())

df["Fecha"] = pd.to_datetime(df["Fecha"])
df["Mes"] = df["Fecha"].dt.to_period("M")

ordenes_por_mes = df.groupby("Mes")["Orden_ID"].count()
print(ordenes_por_mes)

costo_por_mes = df.groupby("Mes")["Costo_Total_PEN"].sum()
print(costo_por_mes.round(2))
