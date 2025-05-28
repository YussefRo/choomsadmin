import pandas as pd


def limpiardf(hoja):

    data = pd.DataFrame(hoja)

    data.columns = [col.strip() for col in data.columns]

    data['Fecha'] = data['Fecha'].str.replace('-','/')
    data['Fecha'] = pd.to_datetime(data['Fecha'], dayfirst=True)

    data = data.query(" Proveedor != '' ")

    data.drop(columns=['No','Semana'],inplace=True)

    return data

def total_venta(data):

    data['Envio'] = data['Envio'].str.replace('$','')
    data['Envio'] = pd.to_numeric(data['Envio'])

    total = data['Envio'].sum()

    return total

def recoleccion(hoja):

    data = pd.DataFrame(hoja)

    data.columns = [col.strip() for col in data.columns]

    data['Fecha'] = data['Fecha'].str.replace('-','/')
    data['Fecha'] = pd.to_datetime(data['Fecha'], dayfirst=True)