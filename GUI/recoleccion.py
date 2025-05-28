import tkinter as tk
from tkinter import ttk
from GoogleSheets import connect_to_sheets
import pandas as pd


class ver_recoleccion(tk.Toplevel):

    def __init__(self,master,dataframe,date, *args, **kwargs):
        super().__init__(*args, master, **kwargs)
        self.con = connect_to_sheets()
        self.sheet = self.con.worksheet("recolecciones")
        self.dataframe = dataframe
        style = ttk.Style()
        color = "provedorFr.TFrame"
        style.configure(color, background="#353535") #FFC0CB
        self.date = date

        self.configure(bg="#353535")
        self.iconbitmap('chooms.ico')
        ancho = 800
        alto = 400
        ancho_pantalla = self.winfo_screenwidth()
        alto_pantalla = self.winfo_screenheight()
        pos_x = (ancho_pantalla // 2) - (ancho // 2)
        pos_y = (alto_pantalla // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{pos_x}+{pos_y}")

        #Da el foco a la nueva ventana
        self.focus()
        self.resizable(False,False)
        # para que se cierre con la x 
        self.protocol("WM_DELETE_WINDIW", self.cerrar)

        self.grid_rowconfigure(0,weight=2)
        self.grid_rowconfigure(1,weight=12)
        self.grid_columnconfigure(0,weight=100)


        frame_tabla = ttk.Frame(self,style=color)
        frame_tabla.grid(row=0,column=0, sticky="nsew", padx=5, pady=5)




        frame_tabla2 = ttk.Frame(self)
        frame_tabla2.grid_propagate(False)
        frame_tabla2.grid(row=1,column=0, sticky="nsew", padx=5, pady=5)

        self.dataframe = self.dataframe[['Fecha', 'Repartidor','Precio_recoleccion','n_paquetes','Proveedor','Domicilio','Telefono']]
        columnas = list(self.dataframe.columns)
        self.tabla = ttk.Treeview(frame_tabla2,columns=columnas,show="headings")
        for col in columnas:
            self.tabla.heading(col,text=col)

        # Crear Scrollbar vertical
        scrollbar_y = ttk.Scrollbar(frame_tabla2, orient="vertical", command=self.tabla.yview)
        scroll_x = ttk.Scrollbar(frame_tabla2, orient="horizontal", command=self.tabla.xview)
        self.tabla.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scroll_x.set)

        self.tabla.grid(row=1,column=0,pady=10,padx=10,sticky='nsew')
        scrollbar_y.grid(row=1, column=1, sticky="ns")
        scroll_x.grid(row=2, column=0, sticky="ew")

        # Permitir expansión
        frame_tabla2.grid_rowconfigure(1, weight=1)
        frame_tabla2.grid_columnconfigure(0, weight=1)

        self.cargar_datos(self.dataframe)


        ttk.Label(frame_tabla,
              text=f"Fecha: {self.date}" ,
              background="#353535",
              font=("Verdana", 12),
              foreground="white").grid(row=0,column=0,padx=5,pady=5)



    def cargar_datos(self,data):

        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        date = pd.to_datetime(self.date)

        data = data.query(" Fecha == @date ")
        data['Fecha'] =  data['Fecha'].dt.strftime('%d-%m-%Y')

        for index, row in data.iterrows():
            self.tabla.insert("","end",values=list(row))

        for col in data.columns:
            max_len = max(
                [len(str(valor)) for valor in data[col]] + [len(col)]
            )
            ancho_px = max_len * 7
            self.tabla.column(col,width=ancho_px, minwidth=ancho_px,stretch=False)


        self.dataframe


    def cerrar(self):
        self.grab_release()
        self.destroy()

