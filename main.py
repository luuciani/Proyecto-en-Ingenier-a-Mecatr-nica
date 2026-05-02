import RPi.GPIO as GPIO
import time
import config
from sensores import Sensores
from motores import Motores
from control import Sistema

GPIO.setmode(GPIO.BCM)

sensores = Sensores(
    config.MAX6675_CSK,
    config.MAX6675_CS,
    config.MAX6675_DO,
    config.FC_EMBOLO,
    config.FC_MOLDE
)

motores = Motores(
    config.DIR_MOTOR1,
    config.STEP_MOTOR1,
    config.DIR_MOTOR2,
    config.STEP_MOTOR2
)

GPIO.setup(config.RELAY, GPIO.OUT)
GPIO.output(config.RELAY, 1)

sistema = Sistema(motores, sensores)

#Para pruebas por colsola / esta parte fue creada por si por algun motivo no se puede ejectutar con GUI. Basicamente es una segunda forma de ejecutarlo
print("Chequeo inicial : ")
print("Temp : ", sensores.leer_temp())
print("Embolo en home : ", sensores.embolo_en_home())
print("Molde cerrado : ", sensores.molde_cerrado())

# Esperar hasta alcanzar 180 °C antes de iniciar
print("Esperando que la temperatura llegue a 180 °C...")
while True:
    temp_actual = sensores.leer_temp()
    print(f"Temp actual: {temp_actual:.2f} °C", end="\r")
    if temp_actual >= 180:
        print("\nTemperatura alcanzada, listo para iniciar.")
        break
    time.sleep(1)

input("Presiona ENTER para iniciar el ciclo ... ") #al presionar enter arranca el proceso de inyección

sistema.iniciar_ciclo()

try:
    while True:
        sistema.ciclo()
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Programa detenido")

finally:
    GPIO.cleanup()

