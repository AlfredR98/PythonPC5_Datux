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
print(dfNew.head(3))

# CASO 2




