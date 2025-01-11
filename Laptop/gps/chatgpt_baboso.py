import time as tm
import pandas as pd

def obtenerDatos(texto):
    texto = texto[7:]
    textos = []
    while texto.find(",") > -1:
        textos.append(texto[:texto.find(",")])
        texto = texto[texto.find(",") + 1:]
    textos.append(texto)  # Agregar el último dato después de la última coma
    return textos

texto = "$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*47"
titulos = ("UTC", "Latitud", "Direccion_latitude", "Longitud",
           "Direccion_longitud", "Calidad", "Numero_SVs", "HDOP",
           "Altura_ortometrica", "Alt_orto_metros", "Separacion_geoide",
           "Sep_geo_metros", "DGPS", "Referencia_estacion_ID",
           "checksum_data")

if __name__ == "__main__":
    if texto[1:6] == "GPGGA":
        datos = obtenerDatos(texto)
        fecha = [str(tm.ctime())]  # Lista con una sola fecha para una sola fila
        tabla = pd.DataFrame([datos], index=fecha, columns=titulos)  # Agregamos datos como lista de una fila
        print(tabla)

