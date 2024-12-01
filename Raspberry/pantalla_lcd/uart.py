import serial
from socket import AF_INET, SOCK_STREAM

#Configurar el puerto UART

ser = serial.Serial('/dev/serial0',9600,timeout=1)
    
while True:
    if ser.in_waiting>0:
        data= ser.readline().decode('utf-8').rstrip()
        print(f"Datos recibidos: {data}")