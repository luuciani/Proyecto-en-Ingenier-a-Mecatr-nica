import RPi.GPIO as GPIO
import time

class Motores:
    def __init__(self, dir1, step1, dir2, step2, logger=print):
        self.dir1 = dir1
        self.step1 = step1
        self.dir2 = dir2
        self.step2 = step2
        self.logger = logger

        GPIO.setup(self.dir1, GPIO.OUT)
        GPIO.setup(self.step1, GPIO.OUT)
        GPIO.setup(self.dir2, GPIO.OUT)
        GPIO.setup(self.step2, GPIO.OUT)

    # MOVIMIENTO GENERAL
    def mover(self, dir_pin, step_pin, direccion, pasos, delay, stop_cond=None):
        GPIO.output(dir_pin, direccion)
        for _ in range(pasos):
            if stop_cond is not None and stop_cond():
                self.logger(" Detenido por final de carrera")
                break
            GPIO.output(step_pin, 1)
            time.sleep(delay)
            GPIO.output(step_pin, 0)
            time.sleep(delay)

    #---------------------------------------
    # MOLDE
    # 1) CIERRE 
    def cerrar_molde(self, delay, stop_cond):
        self.logger("Cerrando molde")
        GPIO.output(self.dir1, 0)  # IMPORTANTE NO CAMBIARLO DE SENTIDO
        while True:
            if stop_cond():
                self.logger("Molde cerrado")
                break
            GPIO.output(self.step1, 1)
            time.sleep(delay)
            GPIO.output(self.step1, 0)
            time.sleep(delay)

    # 2) APERTURA 
    def abrir_molde(self, pasos, delay):
        self.logger("Abriendo molde")
        GPIO.output(self.dir1, 1) #TAMBIEN ES IMPORTANTE NO CAMBIARLO
        for _ in range(pasos):
            GPIO.output(self.step1, 1)
            time.sleep(delay)
            GPIO.output(self.step1, 0)
            time.sleep(delay)
        self.logger("Molde abierto")

    #---------------------------------------
    # ÉMBOLO
    # 1) PRE CARGA (LLEVO MATERIAL HASTA LA MITAD DEL CILINDRO ASI ESTÁ MAS CERCA DE LA RESISTENCIA)
    def pre_carga(self, pasos, delay):
        self.logger("Pre-carga")
        self.mover(self.dir2, self.step2, 0, pasos, delay)
    
    #2)INYECCIÓN (AVANZA EL ÉMBOLO HASTA EL FINAL DEL RECORRIDO, INYECTANDOEL MATERIAL EN EL MOLDE)
    def inyectar(self, pasos, delay):
        self.logger("Inyectando")
        self.mover(self.dir2, self.step2, 0, pasos, delay)
    
    #RETORNO (ÉMBOLO VUELVE A HOME)
    def retorno_embolo(self, delay, stop_cond):
        self.logger("Retorno émbolo")
        GPIO.output(self.dir2, 1)  # TAMPOCO TOCARR
        while not stop_cond():
            GPIO.output(self.step2, 1)
            time.sleep(delay)
            GPIO.output(self.step2, 0)
            time.sleep(delay)
        self.logger("Émbolo en home")

