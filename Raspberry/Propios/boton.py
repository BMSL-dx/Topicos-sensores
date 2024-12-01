from gpiozero import Button,LED
from signal import pause

boton = Button(27)
led = LED(17)

'''
while True:
    if boton.is_pressed:
        print("El boton esta presionado")
    else:
        print("El boton no esta presionado")
'''
def say_hello():
    print("Hola")
    led.on()

def say_goodbye():
    print("Adios")
    led.off()
    
print("Programa listo")
boton.wait_for_press()
print("El boton fue presionado por primera vez")    
boton.when_pressed = say_hello
boton.when_released = say_goodbye

pause() # Sirve para correr las funciones de arriba cada que son realizados
