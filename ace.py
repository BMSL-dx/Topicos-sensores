import smbus
import math

#Parametros de configuracion del sensor en base de la hoja de datos

ACCEL_CONFIG = 0X1C
PWR_MDMT_1   = 0X68
ACCEL_XOUT_H = 0X3B
ACCEL_YOUT_H = 0X3D
ACCEL_ZOUT_H = 0X3F
GYRO_XOUT_H  = 0X43
GYRO_YOUT_H  = 0X45
GYRO_ZOUT_H  = 0X47

def MPU_Init():
    bus.write_byte_data(Device_Address, CONFIG, 3)
    bus.write_byte_data(Device_Address, PWR_MGMT_1, 0)
    bus.write_byte_data(Device_Address, ACCEL_CONFIG, 16)
    
def read_raw_data(addr):
    high = bus.read_byte_data(Device_Address, addr)
    low = bus.read_byte_data(Device_Address, addr+1)
    
    value = ((high<<8) | low)
    
bus = smbus.SMBus(1)
Device_Address = 0x68

MPU_Init()
print("Leyendo datos del acelerometro")

while True:
    
    #Lectura de datos calibrados en base a este sensor en especifico
    
    acc_x = read_raw_data(ACCEL_XOYT_H)
    ac_x = acc_x
    acc_y = read_raw_data(ACCEL_YOYT_H)
    ac_y = acc_y
    acc_z = read_raw_data(ACCEL_ZOYT_H)
    ac_z = acc_z
    #lectura del angulo de inclinacion, para este caso en especifico es a
    
    #impresion de los daos de salida
    #print("\tAx=%.2f",%ac_x,"\tAy=%.2f",%ac_y,"\tAz=%.2f",%ac_z)
    print(f"\tAx={ac_x}\n\tAy={ac_y}\n\tAz={ac_z}")