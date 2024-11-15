import serial
import time
from smbus2 import SMBus
from RPLCD.i2c import CharLCD

# Configuración de la pantalla LCD por I2C
DEVICE_ADDRESS = 0x27
Bus = SMBus(1)
lcd = CharLCD(i2c_expander='PCF8574',address=0x27,cols=16,rows=2)
lcd.write_string('Hola topicos')

# Configurar puerto UART
ser = serial.Serial('/dev/serial0',9600,timeout=1)

while True:
    try:
        if ser.in_waiting>0:
            data = ser.readline().decode('utf-8').rstrip()
            print("Información enviada: ", data)
            lcd.clear()
            # lcd.write_string("dato: "+data)
            volt=float(data)*3.3/65535
            # print(f"Volataje = {volt}")
            rs_ro=(5/volt)-1
            mg_l=0.354*(rs_ro**-1.518)
            lcd.write_string("Volt = "+str(round(volt,4)))
            lcd.cursor_pos(1,0)
            lcd.write_string(f"mg/l={round(mg_l,4)})
    except KeyboardInterrupt:
        print("\nTerminaste el programa a proposito")
        exit(-1)
    except:
        print("Algo salio mal")
        ser = serial.Serial('/dev/serial0',9600,timeout=1)
        time.sleep(0.5)    
