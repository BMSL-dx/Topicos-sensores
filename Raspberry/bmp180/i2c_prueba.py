from smbus2 import SMBus
import time

bus = SMBus(1) # Establece comunicación con el puerto I2C de la Raspberry

# Constantes
DEVICE_ADDRESS,REGISTRO,GET_DATO = 0x77,0xf4,0xf6
OSS,Po = 3,1013.25

# Obtiene los valore de la tabla de calibración de coeficientes
def configure_short(code):
    msb=bus.read_byte_data(DEVICE_ADDRESS,code)
    lsb=bus.read_byte_data(DEVICE_ADDRESS,code+1)
    # print(f"Valor de {hex(code)} = {hex(msb)}")
    # print(f"Valor de {hex(code+1)} = {hex(lsb)}")
    value = (msb << 8) + lsb
    if value & (1<<15):
        value -= 1<<16
    print(f"value {hex(code)} = {value}") # Solo use esto para ver si si recorria bien los datos
    return value

def configure_unsigned(code):
    msb=bus.read_byte_data(DEVICE_ADDRESS,code)
    lsb=bus.read_byte_data(DEVICE_ADDRESS,code+1)
    # print(f"Valor de {hex(code)} = {hex(msb)}")
    # print(f"Valor de {hex(code+1)} = {hex(lsb)}")
    value = (msb << 8) + lsb
    print(f"value {hex(code)} = {value}") # Solo use esto para ver si si recorria bien los datos
    return value
    
"""
# Función en desuso        
def read_data(modo):    
    bus.write_byte_data(DEVICE_ADDRESS,REGISTRO,modo)
    data=bus.read_byte_data(DEVICE_ADDRESS,GET_DATO)
    print(f"Datos leidos de {modo}: {data}")
"""

def temperatura():
    bus.write_byte_data(DEVICE_ADDRESS,REGISTRO,0x2e)
    time.sleep(0.05)
    msb=bus.read_byte_data(DEVICE_ADDRESS,GET_DATO)
    lsb=bus.read_byte_data(DEVICE_ADDRESS,GET_DATO+1)
    ut=(msb<<8)+lsb
    # print(f"Dato bruto temperatura: {ut}")
    x1=((ut-coeficientes["ac6"])*coeficientes["ac5"])>>15
    # print(f"x1 = {x1}")
    x2=(coeficientes["mc"]<<11)/(x1+coeficientes["md"])
    # print(f"x2 = {x2}")
    b5=x1+x2
    # print(f"b5 = {b5}\n")
    temp=(int(b5+8))>>4
    return b5,temp/10

def presion(b5):
    bus.write_byte_data(DEVICE_ADDRESS,REGISTRO,0x34+(OSS<<6))
    msb=bus.read_byte_data(DEVICE_ADDRESS,GET_DATO)
    lsb=bus.read_byte_data(DEVICE_ADDRESS,GET_DATO+1)
    xlsb=bus.read_byte_data(DEVICE_ADDRESS,GET_DATO+2)
    up=((msb<<16) + (lsb<<8) + xlsb)>>(8-OSS)
    # print(f"Dato bruto presion: {up}")
    b6=b5-4000
    x1=(( int( coeficientes["b2"]*(b6**2)) )>>12)>>11
    x2=(coeficientes["ac2"]*b6)
    x3=( int((x1+x2)+2) )>>2
    b3=(((coeficientes["ac1"]*4 + x3)>>OSS)+2)/4
    x1=( int(coeficientes["ac3"]*b6) )>>13
    x2=(( int( coeficientes["b2"]*(b6**2)) )>>12)>>16
    x3=((x1+x2)+2)>>2
    b4=(coeficientes["ac4"]*((x3+32768)&0xffffffff))>>15
    b7=(( int(up-b3) )&0xffffffff)*(50000>>OSS)
    if b7<0x80000000:
        p=(b7*2)/b4
    else:
        p=(b7/b4)*2
    x1=( int(p) >>8)*( int(p) >>8)
    x1=(x1*3038)>>16
    x2=int(-7357*p) >>16
    p=p + (int(x1+x2+3791)>>4)
    return p/100

def altura(p):
    altitude=44330*(1-((p/Po)**(1/5.255)))
    return altitude
    
if __name__=="__main__":
    
    nombres=["ac1","ac2","ac3","ac4","ac5","ac6",
             "b1","b2","mb","mc","md"]
    direcciones=[0xaa,0xac,0xae,0xb0,0xb2,0xb4,0xb6,0xb8,
                 0xba,0xbc,0xbe]

    coeficientes={}
    for (num,name) in enumerate(nombres):
        if (name=="ac4") or (name=="ac5") or (name=="ac6"):
            coeficientes[name]=configure_unsigned(direcciones[num])
        else:
            coeficientes[name]=configure_short(direcciones[num])
    time.sleep(0.1)
    print("")
    
    while True:
        try:
            b5,t=temperatura()
            time.sleep(0.5)
            p=presion(b5)
            time.sleep(0.5)
            al=altura(p)
            print(f"Temperatura = {t}C\nPresión = {p}mbar")
            print(f"Altura = {al}\n")
        except KeyboardInterrupt:
            print("\nPrograma finalizado a proposito.")
            exit(-1)
        except Exception as e:
            print(f"La cagaste: {e}")
