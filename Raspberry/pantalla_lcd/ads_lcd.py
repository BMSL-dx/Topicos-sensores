from smbus2 import SMBus
from RPLCD.i2c import CharLCD
import time

DEVICE_ADDRESS = 0x27
bus = SMBus(1)

lcd = CharLCD(i2c_expander='PCF8574',address=0x27,cols=16,rows=2)
lcd.write_string('Hola Mundo')

DEV_ADDR=0x48
CONVERT_REG,CONFIG_REG=0x00,0x01
os,mux,PGA,MODE,DR=0x0,0x0,0x0,0x0,0x2
COMP=0b00011
config_value1=(os<<17)|(mux<<4)|(PGA<<1)|MODE
config_value2=(DR<<5)|COMP

# Configuración de el ADC
bus.write_i2c_block_data(DEV_ADDR,CONFIG_REG,[config_value1,config_value2])
time.sleep(0.002)

def leer_adc():
    data=bus.read_i2c_block_data(DEV_ADDR,CONVERT_REG,2)
    raw_adc = (data[0]<<8) | data[1]
    #print(f"raw_adc: {raw_adc}")
    #Ajuste si el valor es negativo
    #if raw_adc > 32767:
    #    raw_adc -= 65536 
    return raw_adc


while True:
    valor = leer_adc()
    voo=valor*6.144/32767
    # print(f"valor: {valor}\nVoltaje: {voltaje}")
    rs_ro = (5/voo)-1
    mg_l=0.354*(rs_ro**-1.518)
    lcd.clear()
    lcd.write_string(f"Voo= {round(voo,4)}")
    lcd.cursor_pos=(1,0)
    lcd.write_string(f"mg/l = {round(mg_l,4)}")
    time.sleep(0.5)
