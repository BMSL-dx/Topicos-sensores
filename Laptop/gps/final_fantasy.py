import socket
from socket import AF_INET, SOCK_STREAM

# HOST = "raspberrypi.local"
HOST = "0.0.0.0"
PORT = 12345

s=socket.socket(AF_INET,SOCK_STREAM)
s.bind((HOST,PORT))
s.listen(1)
client,addr=s.accept()
data = client.recv(1024).decode()
print(f"Mensaje recibido: {data}")

# client_socket.sendall("Mensaje recibido correctamente".encode())

client.close()
s.close()
