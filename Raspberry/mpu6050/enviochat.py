import socket

def send_data_to_server(host="192.168.43.72", port=2222):
    try:
        # Crear un socket TCP/IP
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Conectar al servidor
        client_socket.connect((host, port))
        print(f"Conectado al servidor en {host}:{port}")

        # Enviar datos
        message = "Hola, servidor!"
        client_socket.sendall(message.encode('utf-8'))
        print("Datos enviados.")

        # Cerrar conexión
        client_socket.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    send_data_to_server()
