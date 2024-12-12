import socket
from socket import AF_INET,SOCK_STREAM

HOST = "localhost"
PORT = 12345

with socket.socket(AF_INET,SOCK_STREAM) as s:
    try:
        # while True:
        s.connect((HOST, PORT))
        nota = input("Ingrese el texto")
        nota += "\n"
        s.sendall(nota.encode('utf-8'))
    except KeyboardInterrupt:
        print("Programa finalizado")
    except Exception as e:
        print(e)
    
