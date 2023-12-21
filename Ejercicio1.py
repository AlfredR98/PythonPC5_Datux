'''
Busqueda de Alojamiento en Airbnb.
'''
import pandas as pd 
df = pd.read_csv('./doc_bd/airbnb.csv')

# CASO 1
mejoresH = ((df['reviews'] > 10) & (df['overall_satisfaction'] > 4) & (df['accommodates'] == 4) & (df['bedrooms'] == 3))
df_filter = df[mejoresH]
# Para aquellas habitaciones que tienen la misma puntuación, debemos mostrar antes aquellas con más críticas. Debemos darle 3 alternativas.
dfNew = df_filter.sort_values(['overall_satisfaction','reviews'], ascending=[False,False])
df2 = dfNew.head(3)
print(df2)

# CASO 2

# Las id de las casas de Roberto y Clara son 97503 y 90387 respectivamente

casasP = ((df['room_id'] == 97503) | (df['room_id'] == 90387))
reporteRoberto = df[casasP]
try:
    reporteRoberto.to_excel('./doc_bd/Roberto.xlsx',index=False)
    print('Se generó el excel con éxito')
except Exception as e:
    print('Ocurrió un error: ',e)

# CASO 3
'''
pasar 3 noches
Tiene un presupuesto de 50€  
buscarle las 10 propiedades más baratas, 
habitaciones compartidas (room_type == Shared room), y con mejor puntuación
'''

filtro_diana = ((df['price'] <= 50) & (df['room_type'] == 'Shared room'))
df3 = df[filtro_diana]
casaD = df3.sort_values(['overall_satisfaction'], ascending=[False])
print(casaD.head(10))