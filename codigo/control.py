import time
import RPi.GPIO as GPIO
import config

class Sistema:
    def __init__(self, motores, sensores, logger=print, temporizador_cb=None):
        self.motores = motores
        self.sensores = sensores
        self.logger = logger
        self.temporizador_cb = temporizador_cb
        self.estado = "Sin comenzar"
        self.t_inicio = 0
        self.activo = False

    # INICIO DEL CICLO
    def iniciar_ciclo(self):
        self.logger("PRE CARGA")
        self.estado = "PRE CARGA"
        self.activo = True

    # EMERGENCIA
    def emergencia(self):
        self.logger("PARADA DE EMERGENCIA")
        self.activo = False
        self.estado = "Sin comenzar"
        GPIO.output(config.RELAY, 0)  # apaga resistencia

    # CICLO PRINCIPAL
    def ciclo(self):
        if not self.activo:
            return

        # PRE-CARGA
        if self.estado == "PRE CARGA":
            self.motores.pre_carga(config.PASOS_PRE_CARGA,
                                   config.DELAY_STEP_RAPIDO)
            self.estado = "CIERRE MOLDE"

        # CIERRE DEL MOLDE
        elif self.estado == "CIERRE MOLDE":
            self.logger(f"Estado molde antes: {self.sensores.molde_cerrado()}")
            self.motores.cerrar_molde(delay=config.DELAY_STEP_RAPIDO,
                                      stop_cond=self.sensores.molde_cerrado)
            self.logger(f"Estado molde después: {self.sensores.molde_cerrado()}")

            if not self.sensores.molde_cerrado():
                self.logger("ERROR: el molde no se cerró")
                self.emergencia()
                return

            self.logger("Molde cerrado OK. Calentando")
            self.estado = "CALENTAMIENTO"
            self.t_inicio = time.time()

            # Arranca temporizador de 5 minutos (300 seg)
            if self.temporizador_cb:
                self.temporizador_cb(config.TIEMPO_CALENTAMIENTO)

        # CALENTAMIENTO
        elif self.estado == "CALENTAMIENTO":
            temp = self.sensores.leer_temp()

            if temp < config.SET_TEMP:
                GPIO.output(config.RELAY, 1)   # ON, sigue calentando
            else:
                GPIO.output(config.RELAY, 0)   # OFF, corta resistencia

            if temp > 250:  # limitada por seguridad
                self.emergencia()
                return

            if time.time() - self.t_inicio > config.TIEMPO_CALENTAMIENTO:
                GPIO.output(config.RELAY, 0)   # apaga al terminar calentamiento
                self.estado = "INYECCION"

        # INYECCIÓN
        elif self.estado == "INYECCION":
            if not self.sensores.molde_cerrado():
                self.logger("Molde abierto en inyección")
                self.emergencia()
                return

            self.motores.inyectar(config.PASOS_INYECCION,
                                  config.DELAY_STEP_RAPIDO)
            self.estado = "RETORNO"

        # RETORNO
        elif self.estado == "RETORNO":
            self.motores.retorno_embolo(delay=config.DELAY_STEP_RAPIDO,
                                        stop_cond=self.sensores.embolo_en_home)
            self.estado = "ENFRIAMIENTO"
            self.t_inicio = time.time()

        # ENFRIAMIENTO
        elif self.estado == "ENFRIAMIENTO":
            if time.time() - self.t_inicio > config.TIEMPO_ENFRIAMIENTO:
                self.estado = "APERTURA"

        # APERTURA MOLDE
        elif self.estado == "APERTURA":
            self.motores.abrir_molde(pasos=4000, #calculado con pasos porque no tiene switch
                                     delay=config.DELAY_STEP_RAPIDO)
            self.logger("Ciclo terminado")
            self.estado = "Sin comenzar"
            self.activo = False
            GPIO.output(config.RELAY, 0)  # apaga resistencia al terminar


