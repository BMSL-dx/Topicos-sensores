import serial
import time
import socket
from socket import AF_INET, SOCK_STREAM

HOST = "192.168.16.105"
PORT = 12345

def soloGGA(data):
    if data!='':
        if data.find("GPGGA")!=-1:
            print(f"Datos GGA: {data}")
#Configurar el puerto UART

ser = serial.Serial('/dev/ttyS0',9600,timeout=1)
with socket.socket(AF_INET,SOCK_STREAM) as client_s:
    client_s.connect((HOST,PORT))
    msg="Conexion establecida"
    client_s.sendall(msg.encode())
    while True:
        #try:
        if ser.in_waiting>0:
            data= ser.readline().decode('utf-8').rstrip()
            # soloGGA(data)
            # print(f"Datos recibidos: {data}")
            client_s.sendall(data.encode())
        #except KeyboardInterrupt:
        #    exit(-1)
        #except:
        #    print("Error al leer los datos")
        #    time.sleep(1)
