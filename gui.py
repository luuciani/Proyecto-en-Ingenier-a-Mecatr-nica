import tkinter as tk
import threading
import time
import RPi.GPIO as GPIO

import config
from sensores import Sensores
from motores import Motores
from control import Sistema

# ventana principal 
root = tk.Tk()
root.title("Control de Inyectora")
root.geometry("800x600")

# Imagen de fondo
fondo = tk.PhotoImage(file="fondo.png")
fondo_label = tk.Label(root, image=fondo)
fondo_label.place(x=0, y=0, relwidth=1, relheight=1)

# Inicialización 
GPIO.setmode(GPIO.BCM)
sensores = Sensores(
    config.MAX6675_CSK, config.MAX6675_CS, config.MAX6675_DO,
    config.FC_EMBOLO, config.FC_MOLDE
)
motores = Motores(
    config.DIR_MOTOR1, config.STEP_MOTOR1,
    config.DIR_MOTOR2, config.STEP_MOTOR2
)
GPIO.setup(config.RELAY, GPIO.OUT)
GPIO.output(config.RELAY, 1)   # arranca encendido (activo en alto)

# Etiquetas, botones e imagen de la gráfica
estado_label = tk.Label(root, text="Estado: Sin comenzar",
                        font=("Arial", 16),
                        fg="lightgray",
                        bg="#000000")
estado_label.pack(pady=30)

# Imagen del producto
producto_img = tk.PhotoImage(file="pieza.png")  # debe ser PNG o GIF
producto_img = producto_img.subsample(2,2)
producto_label = tk.Label(root, image=producto_img, bg="#000000")
producto_label.pack(pady=10)

# Label de temperatura
temp_label = tk.Label(root, text="Temp: -- ℃",
                      font=("Arial", 14),
                      fg="lightgray",
                      bg="#000000")
temp_label.pack(pady=20)

# Temporizador
timer_label = tk.Label(root, text="Tiempo restante: --:--",
                       font=("Arial", 14),
                       fg="lightgray",
                       bg="#000000")
timer_label.pack(pady=20)

# Callback para mostrar estado
def mostrar_estado(msg):
    estado_label.config(text=f"Estado: {msg}")

# Temporizador
def iniciar_temporizador(segundos):
    inicio=time.time()

    def actualizar():
        restante=int(segundos - (time.time()- inicio))
        if restante > 0:
            minutos, seg = divmod(restante, 60)
            timer_label.config(text=f"Tiempo restante: {minutos:02d}:{seg:02d}")
            root.after(1000, actualizar)
        else:
            timer_label.config(text="Tiempo restante: 00:00")
            mostrar_estado("Listo para inyección")

    segundos_restantes = [segundos]
    actualizar()

# Crear sistema con logger
sistema = Sistema(motores, sensores, logger=mostrar_estado,
                  temporizador_cb=iniciar_temporizador)

# Actualización de temperatura y habilitación del botón
def actualizar_temp():
    temp = sensores.leer_temp()
    temp_label.config(text=f"Temp: {temp:.2f} ℃")

    if temp >= config.SET_TEMP:   # habilita botón al llegar a la temperatura
        btn_iniciar.config(state="normal")
    else:
        btn_iniciar.config(state="disabled")

    root.after(1000, actualizar_temp)

def ciclo_thread():
    sistema.iniciar_ciclo()
    while sistema.activo:
        sistema.ciclo()
        time.sleep(0.1)

def iniciar_proceso():
    temp_actual = sensores.leer_temp()
    if temp_actual < config.SET_TEMP:
        mostrar_estado(f"Temperatura insuficiente. Esperando {config.SET_TEMP} °C...")
        return

    mostrar_estado("Iniciando proceso")
    threading.Thread(target=ciclo_thread, daemon=True).start()

# Botón para iniciar el proceso (arranca deshabilitado)
btn_iniciar = tk.Button(root, text="Iniciar proceso",
                        command=iniciar_proceso,
                        font=("Arial", 12),
                        bg="gray", fg="white",
                        state="disabled")
btn_iniciar.pack(pady=10)

# Loop principal
actualizar_temp()
root.mainloop()
GPIO.cleanup()











