from smbus2 import SMBus
import time
import socket
from socket import AF_INET,SOCK_STREAM
import struct

bus=SMBus(1)

MPU_ADDRESS = 0x68
MPU_CONFIG, PWR_MGMT_1, MPU_GYRO_XOUT_H = 0x1A, 0x6B, 0x43

HOST="192.168.43.72"
PORT=12345

# gyroScale = 4000.0 / 65535.0
gyroScale = 2000.0 / 32768.0  # Ajustado para rango ±2000°/s
inicio = int(time.perf_counter()*1000)
wx0,wx1,wx2=0,0,0
wy0,wy1,wy2=0,0,0
wz0,wz1,wz2=0,0,0
angleX,angleY,angleZ=0,0,0

def transcurrido():
    return int(time.perf_counter()*1000)-inicio

def leerGiroscopio():
    res = bus.read_i2c_block_data(MPU_ADDRESS, MPU_GYRO_XOUT_H, 6)
    x = (res[0] << 8) | res[1]
    y = (res[2] << 8) | res[3]
    z = (res[4] << 8) | res[5]
    
    # Ajustar valores a enteros con signo
    x = x - 65536 if x > 32767 else x
    y = y - 65536 if y > 32767 else y
    z = z - 65536 if z > 32767 else z
    
    return x, y, z


def calibrar():
    muestras = 1000
    sumX, sumY, sumZ = 0, 0, 0
    
    # Descarta las primeras lecturas
    for _ in range(100):
        leerGiroscopio()
        time.sleep(0.001)

    for _ in range(muestras):
        gyroX, gyroY, gyroZ = leerGiroscopio()
        sumX += gyroX
        sumY += gyroY
        sumZ += gyroZ
        time.sleep(0.001)
    
    return sumX / muestras, sumY / muestras, sumZ / muestras

def configuracion():
    bus.write_byte_data(MPU_ADDRESS, MPU_CONFIG, 0x03)       # Configuración básica
    bus.write_byte_data(MPU_ADDRESS, MPU_CONFIG + 1, 0x18)  # ±2000°/s
    bus.write_byte_data(MPU_ADDRESS, MPU_CONFIG + 2, 0x08)  # ±8g
    bus.write_byte_data(MPU_ADDRESS, PWR_MGMT_1, 0x00)      # Activar el sensor
    time.sleep(0.1)

def ajustarRango360(angle):
    while (angle<0):
        angle +=360
    while(angle>=360):
        angle-=360
    return angle

def ajustarAnguloN(ang):
    angulo=ajustarRango360(ang)
    if angulo>180:
        return angulo-360
    else:
        return angulo

#Sirve para enviarle a la laptop correctamente la información
def enviarMensaje(client,msg,valor):
    msg += "\n"
    client.sendall(msg.encode())
    time.sleep(0.05)
    client.sendall(f"{valor}\n".encode('utf-8'))

def redondear(angulo):
    if angulo<0.00001:
        return 0
    else:
        return angulo
        
def enviarAngulos(client,ang_x,ang_y):
    data = struct.pack("<ff",ang_x,ang_y)
    # print(f"data {data}\n")
    client.send(data)
    #print("Desempquetado: ",struct.unpack("ff",data))
    #time.sleep(0.01)
    
configuracion()
sumX,sumY,sumZ=calibrar()

# Inicialización de tiempos
t0,t1,t2=transcurrido(),transcurrido(),transcurrido()

# Sirve para evitar errores al conectarse a la laptop
conectar=True
while conectar:
    try:
        # HOST = input("Ingrese la dirección ip del servidor: ")
        #PORT = int(input("Ingrese el puerto del socket del servidor: "))
        client_s=socket.socket(AF_INET,SOCK_STREAM)
        client_s.connect((HOST, PORT))
        conectar=False
    except KeyboardInterrupt:
        bus.close()
        client_s.close()
        print("¡Retirada estrategica!")
        exit(-1)
    except Exception as e:
        client_s.close()
        print(f"Algo salió mal al intentar conectarse al servidor\n{e}")


try:
    while True:
        gyroX,gyroY,gyroZ=leerGiroscopio()
        # Convertir velocidades angulares y compensar bias
        wx2 = (gyroX - sumX) * gyroScale
        wy2 = (gyroY - sumY) * gyroScale
        wz2 = (gyroZ - sumZ) * gyroScale

        t2=transcurrido()
        h = (t2 - t0) /(4 * 1000.0)

        angleX += (h / 3.0) * (wx0 + 4 * wx1 + wx2)
        angleY += (h / 3.0) * (wy0 + 4 * wy1 + wy2)
        angleZ += (h / 3.0) * (wz0 + 4 * wz1 + wz2)

        angleX = ajustarRango360(angleX)
        angleY = ajustarRango360(angleY)
        # angleZ = ajustarRango360(angleZ)

        enviarAngulos(client_s,angleX,angleY)
        print(f"Angulo X {angleX}\nAngulo Y {angleY}")
        wx0 = wx1; wx1 = wx2
        wy0 = wy1; wy1 = wy2
        wz0 = wz1; wz1 = wz2

        t0 = t1; t1 = t2

        time.sleep(0.07)
        
except Exception as e:
    print("Programa finalizado:")
    print(e)
