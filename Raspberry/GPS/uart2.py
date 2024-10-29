import serial
import time

def soloGGA(data):
    if data!='':
        if data.find("GGA")!=-1:
            print(f"Datos GGA: {data}")
#Configurar el puerto UART

ser = serial.Serial('/dev/ttyS0',9600,timeout=1)
while True:
    try:
        data= ser.readline().decode('utf-8').rstrip()
        soloGGA(data)
        # print(f"Datos recibidos: {data}")
    except KeyboardInterrupt:
        print("Adios")
        exit(-1)
    except:
        print("Error de conexión")
        ser = serial.Serial('/dev/ttyS0',9600,timeout=1)
        time.sleep(1)
