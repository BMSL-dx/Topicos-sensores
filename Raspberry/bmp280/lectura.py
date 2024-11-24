from smbus2 import SMBus
import time
import socket
from socket import AF_INET,SOCK_STREAM

bus = SMBus(1)

# Constantes    |
BMP280_ADDR,UT_REG,UP_REG = 0x76,0xF7,0xFA

#HOST = "192.168.16.105"
#HOST=input("Ingrese la dirección ip: ")
#PORT = int(input("Ingrese el puerto: "))    
#PORT = 12345

# Obtiene los valores de la tabla de calibración de coeficientes
# con signo
def obtenerShort(DEVICE_ADDRESS,code):
    msb=bus.read_byte_data(DEVICE_ADDRESS,code)
    lsb=bus.read_byte_data(DEVICE_ADDRESS,code+1)
    # print(f"Valor de {hex(code)} = {hex(msb)}")
    # print(f"Valor de {hex(code+1)} = {hex(lsb)}")
    value = (msb << 8) + lsb
    if value & (1<<15):
        value -= 1<<16
    print(f"value {hex(code)} = {value}") # Solo use esto para ver si si recorria bien los datos
    return value

# Obtiene los valores de la tabla de calibración de coeficientes
# sin signo
def obtenerUnsigned(DEVICE_ADDRESS,code):
    msb=bus.read_byte_data(DEVICE_ADDRESS,code)
    lsb=bus.read_byte_data(DEVICE_ADDRESS,code+1)
    # print(f"Valor de {hex(code)} = {hex(msb)}")
    # print(f"Valor de {hex(code+1)} = {hex(lsb)}")
    value = (msb << 8) + lsb
    return  value
    #print(f"value {hex(code)} = {value}") # Solo use esto para ver si si recorria bien los datos

def obtenerSignedLong(DEVICE_ADDRESS,reg):
    msb=bus.read_byte_data(DEVICE_ADDRESS,reg)
    lsb=bus.read_byte_data(DEVICE_ADDRESS,reg+1)
    xlsb=bus.read_byte_data(DEVICE_ADDRESS,reg+2)
    value = (msb << 16) + (lsb << 8) + xlsb
    # print(f"msb {hex(reg)} = {msb}")
    # print(f"lsb {hex(reg+1)} = {lsb}")
    # print(f"xlsb {hex(reg+2)} = {xlsb}")
    if value & (1<<19):
        value -= 1<<20
    return value

# Programa principal del programa

id = bus.read_byte_data(BMP280_ADDR,0xD0)
print(f"id={hex(id)}")
status = bus.read_byte_data(BMP280_ADDR,0xF3)
print(f"status={hex(status)}")
# Escribe en ctrl_meas
bus.write_byte_data(BMP280_ADDR,0xF4,(1<<5)+(1<<2)+(1<<1)+1)
regs=[0x88,0x8A,0x8C,0x8E,0x90,0x92,0x94,0x96,0x98,0x9A,0x9C,0x9E,0xA0]
coeficientes = {}
coeficientes["T1"] = obtenerUnsigned(BMP280_ADDR,regs[0])
for i in range(1,3):
    coeficientes[f"T{i+1}"] = obtenerShort(BMP280_ADDR,regs[i])
coeficientes["P1"] = obtenerUnsigned(BMP280_ADDR,regs[0])
for i in range(2,10):
    coeficientes[f"P{i}"]=obtenerShort(BMP280_ADDR,regs[i+2])
time.sleep(0.1)

if __name__=="__main__":
#with socket.socket(AF_INET,SOCK_STREAM) as client_s:
    #client_s.connect((HOST, PORT))
    for i in coeficientes:
        print(coeficientes[i])
        msg= str(coeficientes[i])+"\n"
        #client_s.sendall(msg.encode())
    while True:
        ut = obtenerSignedLong(BMP280_ADDR,UT_REG)
        up = obtenerSignedLong(BMP280_ADDR,UP_REG)
        print(f"ut={ut}\nup={up}")
        time.sleep(1)
