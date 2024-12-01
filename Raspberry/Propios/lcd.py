from gpiozero import LED,PWMLED
from time import sleep

green = PWMLED(4)
red = LED(17)

try:
    while True:
        red.on()
        green.value=0
        sleep(0.5)
        red.off()
        green.value=0.3
        sleep(0.5)
        green.value=0.6
        red.on()
        sleep(0.5)
        green.value=1
        red.off()
        sleep(0.5)
except KeyboardInterrupt:
    print("\nPrograma teminado")
except:
    print("Error inesperado")
