from tkinter import messagebox
import tkinter as tk
from tkinter import ttk as ttk
from GoogleSheets import connect_to_sheets
from Utils import datos
import pandas as pd
from tkcalendar import DateEntry
import datetime
from GUI import recoleccion



def cargar_datos(data):
    # Limpiar tabla antes de cargar (opcional)
    for fila in tabla.get_children():
        tabla.delete(fila)

    fecha = pd.to_datetime(selector.get_date())

    data = data.query(" Fecha == @fecha ")
    data['Fecha'] = data['Fecha'].dt.strftime('%d-%m-%Y')

    # Insertar los datos del DataFrame
    for index, row in data.iterrows():
        tabla.insert("", "end", values=list(row))

    for col in data.columns:
        max_len = max(
            [len(str(valor)) for valor in data[col]] + [len(col)]
        )  # Mayor entre valores y encabezado
        ancho_px = max_len * 7  # Aproximadamente 7px por carácter
        tabla.column(col, width=ancho_px, minwidth=ancho_px, stretch=False)

    total = datos.total_venta(data)

    total_venta.set(total)
    total_empresa.set(total/2)
    total_repa.set(total/2)

    print(data.groupby('Repartidor')['Envio'].sum()/2)

    ventana_secundaria.destroy()

    

def recolecciones():
    global ventana_secundaria
    if ventana_secundaria is None or not ventana_secundaria.winfo_exists():
        ventana_secundaria = recoleccion.ver_recoleccion(ventana,reco_data,selector.get_date())
    else:
        ventana_secundaria.deiconify()  # La vuelve a mostrar si estaba oculta
        ventana_secundaria.lift()
        ventana_secundaria.focus_force()

if __name__ == "__main__":

    ventana = tk.Tk()

    ventana_secundaria = None
    con = connect_to_sheets()
    sheet = con.worksheet("2025")
    sheet2 = con.worksheet('recolecciones')
    total_venta = tk.StringVar()
    total_empresa = tk.StringVar()
    total_repa = tk.StringVar()

    data = datos.limpiardf(sheet.get_all_records())
    reco_data = datos.limpiardf(sheet2.get_all_records())

    
    print(reco_data)


    ############################################################

    ventana.title("Chooms Admin")

    #poscionar ventana en el centro
    ancho_ventana = 1500
    alto_ventana = 500
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()
    pos_x = (ancho_pantalla // 2) - (ancho_ventana // 2)
    pos_y = (alto_pantalla // 2) - (alto_ventana // 2)
    ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{pos_x}+{pos_y}")
    style = ttk.Style()
    ventana.configure(bg="#353535")

    #configuracion del icono
    ventana.iconbitmap('chooms.ico')

    #ventana no expandible
    ventana.resizable(False, False)

    boton_redondo_pequeno = "RoundedButton_peque.TButton"
    style.configure(boton_redondo_pequeno,
                padding=1,
                relief="flat",
                background="#353535",
                foreground="#353535",
                font=("Arial", 10))


    # Frames
    #######################################################################
    ventana.grid_columnconfigure(0, weight=2)
    ventana.grid_columnconfigure(1, weight=15)

    ventana.grid_rowconfigure(0,weight=6)
    ventana.grid_rowconfigure(1,weight=3)

    frame_tabla = tk.Frame(ventana, background="#353535")
    frame_tabla.grid_propagate(False)
    frame_tabla.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

    
    frame_tabla2 = tk.Frame(ventana, background="white")
    frame_tabla2.grid_propagate(False)
    frame_tabla2.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

    frame_tabla3 = tk.Frame(ventana, background="red")
    frame_tabla3.grid_propagate(False)
    frame_tabla3.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)



    # Tabla
    ##########################################################################

    columnas = list(data.columns)
    tabla = ttk.Treeview(frame_tabla2, columns=columnas, show="headings")
    for col in columnas:
        tabla.heading(col, text=col)

    # Crear Scrollbar vertical
    scrollbar_y = ttk.Scrollbar(frame_tabla2, orient="vertical", command=tabla.yview)
    scroll_x = ttk.Scrollbar(frame_tabla2, orient="horizontal", command=tabla.xview)
    tabla.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scroll_x.set)


    tabla.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
    scrollbar_y.grid(row=1, column=1, sticky="ns")
    scroll_x.grid(row=2, column=0, sticky="ew")

    # Permitir expansión
    frame_tabla2.grid_rowconfigure(1, weight=1)
    frame_tabla2.grid_columnconfigure(0, weight=1)

    # Botones
    ##############################################################################

    
    ttk.Label(frame_tabla,
              text="Fecha",
              background="#353535",
              font=("Verdana", 12),
              foreground="white").grid(row=1,column=0,padx=5,pady=5)



    fecha_inicio = datetime.date(2025,1,1)
    fecha_fin = datetime.date.today()
    selector = DateEntry(frame_tabla,
                        date_pattern="dd-mm-yyyy",
                        mindate=fecha_inicio,
                        maxdate=fecha_fin,
                        state='readonly')
    selector.grid(row=1,column=1,padx=5,pady=5)



    boton_cargar = ttk.Button(frame_tabla, text="Cargar datos", command=lambda:cargar_datos(data), style=boton_redondo_pequeno)
    boton_cargar.grid(row=2,column=1,padx=5,pady=5)

    boton_cargar = ttk.Button(frame_tabla, text="Recolecciones", command=recolecciones, style=boton_redondo_pequeno)
    boton_cargar.grid(row=3,column=1,padx=5,pady=10)

    # Labels
    ###################################################################################

    ttk.Label(frame_tabla3,
              text="Empresa: ",
              background="#353535",
              font=("Verdana", 12),
              foreground="white").grid(row=1, column=1, padx=5, pady=5, sticky="w")
    
    entry_empresa = ttk.Entry(frame_tabla3,textvariable=total_empresa ,width=7, state="readonly",font=("Arial", 12))
    entry_empresa.grid(row=1, column=2, padx=5, pady=5)

    ttk.Label(frame_tabla3,
              text="Repartidores: ",
              background="#353535",
              font=("Verdana", 12),
              foreground="white").grid(row=2, column=1, padx=5, pady=5, sticky="w")
    
    entry_repartidor = ttk.Entry(frame_tabla3,textvariable=total_empresa ,width=7, state="readonly",font=("Arial", 12))
    entry_repartidor.grid(row=2, column=2, padx=5, pady=5)

    ttk.Label(frame_tabla3,
              text="Total Envios: ",
              background="#353535",
              font=("Verdana", 12),
              foreground="white").grid(row=3, column=1, padx=5, pady=5, sticky="w")
    
    entry_precio_producto = ttk.Entry(frame_tabla3,textvariable=total_venta ,width=7, state="readonly",font=("Arial", 12))
    entry_precio_producto.grid(row=3, column=2, padx=5, pady=5)


    ventana.mainloop()

