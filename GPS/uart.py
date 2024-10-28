import serial
import socket
from socket import AF_INET, SOCK_STREAM

HOST = "192.168.43.72"
PORT = 12345

#Configurar el puerto UART

ser = serial.Serial('/dev/serial0',9600,timeout=1)
with socket.socket(AF_INET,SOCK_STREAM) as client_s:
    client_s.connect((HOST,PORT))
    
    while True:
        if ser.in_waiting>0:
            data= ser.readline().decode('utf-8').rstrip()
			# print(f"Datos recibidos: {data}")
            client_s.sendall(data.encode())
