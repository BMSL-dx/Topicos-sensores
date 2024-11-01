import time as tm
import csv
import pandas as pd
import os
import socket
from socket import AF_INET, SOCK_STREAM

def obtenerDatos(texto):
    texto=texto[7:]
    fecha=str(tm.ctime())
    textos=[fecha]
    while texto.find(",")>-1:
        if texto[:texto.find(",")]=="":
            textos.append("Vacio")
        else:
            textos.append(texto[:texto.find(",")])
        texto=texto[texto.find(",")+1:]
    textos.append(texto)
    return textos
    
titulos=("Tiempo","UTC","Latitud","Direccion_latitude","Longitud",
        "Direccion_longitud","Calidad","Numero_SVs","HDOP",
        "Altura_ortometrica","Alt_orto_metros","Separacion_geoide",
        "Sep_geo_metros","DGPS","Referencia_estacion_ID")
        # "checksum_data","algo")

def escribirCSV(datos):
    tabla = pd.DataFrame([datos],columns=list(titulos))
    if os.path.exists('datos_gps.csv'):
        df = pd.read_csv('datos_gps.csv')
        tabla=pd.concat([tabla,df],sort=False,join="inner",
                        ignore_index=True)
    tabla.to_csv('datos_gps.csv')
    print(tabla)

if __name__=="__main__":
    # HOST = "raspberrypi.local"
    HOST = "0.0.0.0"
    PORT = 12345

    with socket.socket(AF_INET,SOCK_STREAM) as s:
        s.bind((HOST,PORT))
        s.listen(5)
        print("Esperando cliente...")
        client,addr=s.accept()
        print(f"cliente {client} aceptado")
        texto = client.recv(1024).decode()
        print(texto)
        while True:
            texto = client.recv(1024).decode()
            # print(f"Mensaje recibido: {data}")
            # if texto!="" or texto!=NaN:
            #     print(texto)

            if texto[3:6]=="GGA":
                datos=obtenerDatos(texto)
                escribirCSV(datos)
                # print(f"GGA={texto}")

        client.close()
       
