from tkinter import *
from tkinter import ttk
import tkinter as tk

class CalibrationInstructions:

    instructions = "Al pulsar el botón calibrar la aplicación ocupará la pantalla completa del ordenador.\n\
Debido a que es necesario calibrar su mirada con las diferentes zonas de la pantalla de su\n\
dispositivo, aparezerán círculos grises en las zonas de calibración.\n\
Centre su mirada en el círculo de color rojo. Cuando tenga la mirada centrada en el círculo rojo,\n\
pulse la barra espaciadora para calibrarlo, verá que el punto se vuelve naranja. Cuando se complete el calibrado del punto\n\
este se volverá de color verde, centre de nuevo la mirada en el próximo punto rojo y repita el proceso hasta.\n\
completar el calibrado.\n\n\
El botón de Play iniciará la grabación desde la cámara, sin calibrado. Asegúrese de contar con\n\
buena luz y sitúese de tal forma que el programa reconozca sus ojos el mayor tiempo posible\n\n\
El botón de Stop detendrá tanto la grabación como el calibrado.\n"

    def show_instructions_popup(self, tab):
        self.popup = Toplevel(tab)
        self.popup.geometry("600x400")
        self.popup.title("Instrucciones de calibrado")

        h1 = Label(self.popup, text="INSRTUCCIONES DE CALIBRADO", font=("Helvetica", 12, "bold"), pady=20)
        label = Label(self.popup, text=self.instructions, justify="left")
        h1.pack()
        label.pack()