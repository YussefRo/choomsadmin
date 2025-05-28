import tkinter as tk
from tkinter import messagebox
import gspread
from oauth2client.service_account import ServiceAccountCredentials

#arch_json = "credenciales_yusa.json"  #archivo json de prueba
arch_json = "credenciales.json"

#nom_hoja = "pruebaChoms"   #hoja de prueba
nom_hoja = "vaciado-informacion-2025"

def connect_to_sheets():
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(arch_json, scope)
        client = gspread.authorize(creds)
        return client.open(nom_hoja)  # Cambia el nombre a tu hoja
    except Exception as e:
        print(e)
        messagebox.showerror("Error", f"No se pudo conectar a Google Sheets: {e}")
        return None