import serial
import time
import socket
from socket import AF_INET, SOCK_STREAM

#HOST = "192.168.43.72"
HOST = input("Ingrese la dirección ip")
PORT = 12345

# Configurar el puerto UART
ser = serial.Serial('/dev/ttyS0',9600,timeout=1)
with socket.socket(AF_INET,SOCK_STREAM) as client_s:
    client_s.connect((HOST,PORT))
    msg="Conexion establecida"
    client_s.sendall(msg.encode())
    while True:
        try:
            data= ser.readline().decode('utf-8').rstrip()
            # print(f"Datos recibidos: {data}")
            client_s.sendall(data.encode())
        except KeyboardInterrupt:
            exit(-1)
        except:
            print("Error al leer los datos")
            ser = serial.Serial('/dev/ttyS0',9600,timeout=1)
            time.sleep(1)
