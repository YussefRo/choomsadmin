import tkinter as tk
from tkinter import ttk

class contabilidad(tk.Toplevel):

    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)
        self.title("Hola")
        print("sdasd")

            #poscionar self en el centro
        ancho_self = 950
        alto_self = 650
        ancho_pantalla = self.winfo_screenwidth()
        alto_pantalla = self.winfo_screenheight()
        pos_x = (ancho_pantalla // 2) - (ancho_self // 2)
        pos_y = (alto_pantalla // 2) - (alto_self // 2)
        self.geometry(f"{ancho_self}x{alto_self}+{pos_x}+{pos_y}")
        self.configure(bg="#353535")

        #configuracion del icono
        #self.iconbitmap('chooms.ico')

        #self no expandible
        self.resizable(False, False)
