import RPi.GPIO as GPIO
import MAX6675.MAX6675 as MAX6675
import time


class Sensores:
    def __init__(self, csk, cs, do, fc_embolo, fc_molde):
        self.sensor_temp = MAX6675.MAX6675(csk, cs, do)

        self.fc_embolo = fc_embolo
        self.fc_molde = fc_molde

        GPIO.setup(self.fc_embolo, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.fc_molde, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # TEMPERATURA 
    def leer_temp(self):
        temp = self.sensor_temp.readTempC()
        time.sleep(0.3)
        return temp


    # FINALES DE CARRERA (CONFIG. PARA: EMBOLO HOME Y MATRIZ CERRADA)
    def molde_cerrado(self):
        estado = GPIO.input(self.fc_molde) == 1
        print(f"[DEBUG] Molde cerrado: {estado}")
        return estado

    def embolo_en_home(self):
        lecturas = [GPIO.input(self.fc_embolo) for _ in range(5)]
        estado = sum(lecturas) >= 3
        print(f"[DEBUG] Embolo home: {estado}")
        return estado
