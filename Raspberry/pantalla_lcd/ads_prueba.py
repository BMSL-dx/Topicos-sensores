from smbus2 import SMBus
import time

bus = SMBus(1)

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
    voltaje=valor*6.144/32767
    rs_ro = (5/voltaje)-1
    mg_l=0.354*(rs_ro**-1.518)
    print(f"valor: {valor}\nVoltaje: {voltaje}\nmg/l: {mg_l}")
    time.sleep(0.25)
