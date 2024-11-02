from smbus2 import SMBus
import time
import socket
from socket import AF_INET,SOCK_STREAM

bus = SMBus(1) # Establece comunicación con el puerto I2C de la Raspberry

# Constantes
DEVICE_ADDRESS,REGISTRO,GET_DATO = 0x77,0xf4,0xf6
OSS,OSD,Po = 3,0.05,1013

# Obtiene los valores de la tabla de calibración de coeficientes
# con signo
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

# Obtiene los valores de la tabla de calibración de coeficientes
# sin signo
def configure_unsigned(code):
    msb=bus.read_byte_data(DEVICE_ADDRESS,code)
    lsb=bus.read_byte_data(DEVICE_ADDRESS,code+1)
    # print(f"Valor de {hex(code)} = {hex(msb)}")
    # print(f"Valor de {hex(code+1)} = {hex(lsb)}")
    value = (msb << 8) + lsb
    print(f"value {hex(code)} = {value}") # Solo use esto para ver si si recorria bien los datos
    return value

# Forza a un número a tener valores de 32 bits
def bits32(numero):
    num=int(numero)
    return (num & 0xffffffff)

# Esfunción sirve para obtener la temperatura y convertirla a valores
# en Celcius
def temperatura():
    bus.write_byte_data(DEVICE_ADDRESS,REGISTRO,0x2e)
    time.sleep(0.005)
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
    temp=(bits32(b5+8))>>4
    return b5,temp/10

# Esta función obitene el valor de la presión del modulo y la
# convierte en valores de m
def presion(b5):
    bus.write_byte_data(DEVICE_ADDRESS,REGISTRO,0x34+(OSS<<6))
    time.sleep(OSD)
    msb=bus.read_byte_data(DEVICE_ADDRESS,GET_DATO)
    lsb=bus.read_byte_data(DEVICE_ADDRESS,GET_DATO+1)
    xlsb=bus.read_byte_data(DEVICE_ADDRESS,GET_DATO+2)
    up=((msb<<16) + (lsb<<8) + xlsb)>>(8-OSS)
    # print(f"Dato bruto presion: {up}")
    b6=b5-4000
    x1=(( bits32(coeficientes["b2"]*(b6**2)) )>>12)>>11
    x2=(coeficientes["ac2"]*b6)
    x3=( bits32((x1+x2)+2) )>>2
    b3=(((coeficientes["ac1"]*4 + x3)>>OSS)+2)/4
    x1=( bits32(coeficientes["ac3"]*b6) )>>13
    x2=(( bits32(coeficientes["b2"]*(b6**2)) )>>12)>>16
    x3=((x1+x2)+2)>>2
    b4=(coeficientes["ac4"]*((x3+32768)&0xffffffff))>>15
    b7=(( bits32(up-b3) )&0xffffffff)*(50000>>OSS)
    if b7<0x80000000:
        p=(b7*2)/b4
    else:
        p=(b7/b4)*2
    x1=( bits32(p) >>8)*( bits32(p) >>8)
    x1=(x1*3038)>>16
    x2=bits32(-7357*p) >>16
    p=p + (( bits32(x1+x2+3791) )>>4)
    return p/100

# Obtiene el valor de la altura en base a la presión calculada
def altura(p):
    altitude=44330*(1-((p/Po)**(1/5.255)))
    return altitude

# Convierte a otro sistema de unidades los valores
def conversiones(t,p,a):
    far = (1.8*t) + 32
    hg = p*0.0295200830714
    foots = a*3.28084
    return far,hg,foots

#Sirve para enviarle a la laptop correctamente la información
def enviar_mensaje(client,msg,valor):
    msg += "\n"
    client.sendall(msg.encode())
    time.sleep(0.05)
    #valor_codificado=str(valor).encode
    client.sendall(f"{valor}\n".encode('utf-8'))

# Función principal
if __name__=="__main__":
    
    nombres=["ac1","ac2","ac3","ac4","ac5","ac6",
             "b1","b2","mb","mc","md"]
    direcciones=[0xaa,0xac,0xae,0xb0,0xb2,0xb4,0xb6,0xb8,
                 0xba,0xbc,0xbe]

    coeficientes={}
    try:
        # Se obtiene la tabla de constantes de calibración
        for (num,name) in enumerate(nombres):
            if (name=="ac4") or (name=="ac5") or (name=="ac6"):
                coeficientes[name]=configure_unsigned(direcciones[num])
            else:
                coeficientes[name]=configure_short(direcciones[num])
    except Exception as e:
        print("Algo salió mal al asignar la tabla de" +
              f"calibración de coeficientes\n{e}")
        exit(-1)
        
    time.sleep(0.1)
    print("")

    # Sirve para evitar errores al conectarse a la laptop
    conectar=True
    while conectar:
        try:
            HOST="192.168.43.72"
            # HOST = input("Ingrese la dirección ip del servidor: ")
            PORT = int(input("Ingrese el puerto del socket del servidor: "))
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

    # Parte principal del programa
    while True:
        try:
            b5,t=temperatura()
            p=presion(b5)
            al=altura(p)
            temp2,pres2,alt2 =conversiones(t,p,al)
            enviar_mensaje(client_s,"Temperatura",t)
            enviar_mensaje(client_s,"Presion",p)
            enviar_mensaje(client_s,"Altura",al)
            enviar_mensaje(client_s,"Temp2",temp2)
            enviar_mensaje(client_s,"Pres2",pres2)
            enviar_mensaje(client_s,"Alt2",alt2)
            # print(f"Temperatura = {t}C\nPresión = {p}mbar")
            # print(f"Altura = {al}\n")
            time.sleep(0.5)
        except KeyboardInterrupt:
            msg="Adios_garuda\n"
            client_s.sendall(msg.encode())
            client_s.close()
            bus.close()
            print("\nPrograma finalizado a proposito.")
            exit(-1)
        except Exception as e:
            print(f"No se pueden leer los valores por alguna razon\n{e}")
            time.sleep(1)
