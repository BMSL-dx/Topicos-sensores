import pandas as pd
import time as tm

'''
while True:
    df = pd.read_csv('datos_gps.csv') 
    primeros = df.head(5)
    longitud = df['Latitud'].iloc[0]-df['Latitud'].iloc[1]
    latitud = df['Longitud'].iloc[0]-df['Longitud'].iloc[1]

    velocidad = ((longitud**2)+ (latitud**2))**(1/2)

    print(f"Velocidad = {velocidad}")
    tm.sleep(1)
'''

df=pd.read_csv('datos_gps.csv')
print(df[['Latitud','Longitud','Altura_ortometrica']])
# print(df['Longitud'])
# print(df['Altura_ortometrica'])
