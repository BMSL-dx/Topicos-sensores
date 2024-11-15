from smbus2 import SMBus
from RPLCD.i2c import CharLCD

DEVICE_ADDRESS = 0x27
bus = SMBus(1)

lcd = CharLCD(i2c_expander='PCF8574',address=0x27,cols=16,rows=2)
lcd.write_string('Hola Mundo')

while True:
    texto = input("Ingrese el texto que desee mostrar: ")
    lcd.clear()
    lcd.write_string(texto)

print("Hola mundo")
