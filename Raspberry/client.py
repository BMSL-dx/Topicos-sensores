import socket
from socket import AF_INET,SOCK_STREAM

HOST = "192.168.16.105"
#HOST=input("Ingrese la dirección ip: ")
PORT = int(input("Ingrese el puerto: "))
with socket.socket(AF_INET,SOCK_STREAM) as client_s:
    client_s.connect((HOST, PORT))
    try:
        while 1:
            msg=input("Envia un mensaje: ")
            msg+="\n"
            client_s.sendall(msg.encode())
    except KeyboardInterrupt:
        msg="Adios_garuda\n"
        client_s.sendall(msg.encode())
        print("Programa terminado")
    except:
        print("Algo salio mal")
        exit(-1)    
    
    
