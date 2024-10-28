import serial
import time

def soloGGA(data):
    if data!='':
        if data.find("GPGGA")!=-1:
            print(f"Datos GGA: {data}")
#Configurar el puerto UART

ser = serial.Serial('/dev/ttyS0',9600,timeout=1)
while True:
    try:
        if ser.in_waiting>0:
            data= ser.readline().decode('utf-8').rstrip()
            # soloGGA(data)
            print(f"Datos recibidos: {data}")
    except KeyboardInterrupt:
        exit(-1)
    except:
        print("Error al leer los datos")
        ser = serial.Serial('/dev/ttyS0',9600,timeout=1)
        time.sleep(1)
