from smbus2 import SMBus
import time

# Dirección I2C del ADS1115 (generalmente 0x48, pero podría variar)
ADS1115_ADDRESS = 0x48

# Registros y configuraciones del ADS1115
REG_CONVERT = 0x00  # Registro para leer la conversión
REG_CONFIG = 0x01   # Registro de configuración

# Valores de configuración
CONFIG_OS_SINGLE = 0x8000      # Realizar una sola conversión
CONFIG_MUX_AIN0 = 0x4000       # Mux para canal A0
CONFIG_GAIN = 0x0200           # Ganancia (por ejemplo, +/- 4.096V)
CONFIG_MODE_SINGLE = 0x0100    # Modo de conversión de una sola vez
CONFIG_DR_1600SPS = 0x0080     # Tasa de datos de 1600 muestras por segundo

# Combinación final para el registro de configuración del canal A0
CONFIG_A0 = (CONFIG_OS_SINGLE | CONFIG_MUX_AIN0 | CONFIG_GAIN |
             CONFIG_MODE_SINGLE | CONFIG_DR_1600SPS)

def read_adc(channel):
    with SMBus(1) as bus:
        # Configurar el canal y comenzar la conversión
        config = CONFIG_A0 if channel == 0 else None  # Solo configuramos para A0 en este ejemplo
        bus.write_i2c_block_data(ADS1115_ADDRESS, REG_CONFIG, [(config >> 8) & 0xFF, config & 0xFF])

        # Espera el tiempo necesario para la conversión (aproximadamente 1ms para 1600SPS)
        time.sleep(0.001)

        # Leer el resultado de la conversión
        data = bus.read_i2c_block_data(ADS1115_ADDRESS, REG_CONVERT, 2)
        # Combina los bytes de resultado
        raw_adc = data[0] << 8 | data[1]
        
        # Ajuste si el valor es negativo (por ser de 16 bits)
        if raw_adc > 0x7FFF:
            raw_adc -= 0x10000
        
        return raw_adc

# Ejemplo de uso: Leer el valor del canal A0
valor_a0 = read_adc(0)
print(f"Valor del canal A0: {valor_a0}")
