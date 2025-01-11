from smbus2 import SMBus
import time

bus=SMBus(1)

MPU_ADDRESS = 0x68
MPU_CONFIG, PWR_MGMT_1, MPU_GYRO_XOUT_H = 0x1A, 0x6B, 0x43

gyroScale = 4000.0 / 65535.0
inicio = int(time.perf_counter()*1000)
wx0,wx1,wx2=0,0,0
wy0,wy1,wy2=0,0,0
wz0,wz1,wz2=0,0,0
angleX,angleY,angleZ=0,0,0

def transcurrido():
    return int(time.perf_counter()*1000)-inicio

def leerGiroscopio():
    res=bus.read_i2c_block_data(MPU_ADDRESS,MPU_GYRO_XOUT_H,6)
    # print(res)
    x=(res[0]<<8) + res[1]
    y=(res[2]<<8) + res[3]
    z=(res[4]<<8) + res[5]
    # print(f"x={x}\ny={y}\nz={z}")
    # print(f"{bin(x)}\n{bin(y)}\n{bin(z)}")
    return x,y,z


def calibrar():
    muestras=1000
    sumX,sumY,sumZ=0,0,0
    for i in range(muestras):
        gyroX,gyroY,gyroZ=leerGiroscopio()
        sumX += gyroX
        sumY += gyroY
        sumZ += gyroZ
        time.sleep(0.01)
    sumX /= muestras
    sumY /= muestras
    sumZ /= muestras
    print(f"X {sumX}\nY {sumY}\nZ {sumZ}")
    return sumX,sumY,sumZ        

def configuracion():
    bus.write_byte_data(MPU_ADDRESS,MPU_CONFIG,0x03)
    bus.write_byte_data(MPU_ADDRESS,MPU_CONFIG+1,0x18)
    bus.write_byte_data(MPU_ADDRESS,MPU_CONFIG+2,0x18)
    bus.write_byte_data(MPU_ADDRESS,PWR_MGMT_1,0)

def ajustarRango360(angle):
    while (angle<0):
        angle +=360
    while(angle>=360):
        angle-=360
    return angle

configuracion()
sumX,sumY,sumZ=calibrar()

# Inicialización de tiempos
t0,t1,t2=transcurrido(),transcurrido(),transcurrido()

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

    """
    angleX = ajustarRango360(angleX)
    angleY = ajustarRango360(angleY)
    angleZ = ajustarRango360(angleZ)
    """

    print(type(angleX))
    print(f"Angle X: {angleX}\nAngle Y: {angleY}\nAngle Z: {angleZ}")
    
    wx0 = wx1; wx1 = wx2
    wy0 = wy1; wy1 = wy2
    wz0 = wz1; wz1 = wz2

    t0 = t1; t1 = t2

    time.sleep(0.05)
