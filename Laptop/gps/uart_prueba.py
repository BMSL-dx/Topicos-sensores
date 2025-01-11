from machine import UART, Pin

# Inicializa el UART en el puerto 1, con baudrate de 9600
uart1 = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))

# Bucle infinito para leer datos
while True:
    if uart1.any():  # Verifica si hay datos disponibles para leer
        data = uart1.read()  # Lee los datos
        if data:
            print('Datos recibidos:', data.decode('utf-8'))  # Muestra los datos recibidos

