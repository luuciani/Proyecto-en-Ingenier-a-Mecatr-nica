# CONFIGURACIÓN GENERAL// ACÁ INDICO QUE COSA VA A CADA PIN DE RASPBERRY Y PARÁMETROS BÁSICOS

# Pines de cada motor
DIR_MOTOR1 = 19
STEP_MOTOR1 = 13

DIR_MOTOR2 = 27
STEP_MOTOR2 = 4

# Pines finales de carrera (NC)
FC_EMBOLO = 17
FC_MOLDE = 22

# Termocupla MAX6675
MAX6675_CSK = 25
MAX6675_CS = 24
MAX6675_DO = 18

# Relé resistencia
RELAY = 26

# Parámetros de proceso
SET_TEMP = 50 #Temperatura de fundicion del polipropileno
TIEMPO_CALENTAMIENTO = 300 #5 min
TIEMPO_ENFRIAMIENTO = 20 #20 seg y se separa el molde del pico

# Movimiento
PASOS_PRE_CARGA = 5850
PASOS_INYECCION = 5850

# Velocidad 
DELAY_STEP_RAPIDO = 0.0005 #Calculados en base al mejor funcionamiento del motor
DELAY_STEP_LENTO = 0.0005
