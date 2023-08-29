import pandas as pd
from datetime import datetime
import os
import numpy as np

from math import radians, sin, cos, sqrt, atan, tan, atan2

# Esta funcion es una implementación de la fórmula de Vincenty para calcular la distancia entre dos puntos
# en la superficie de un elipsoide, utilizando sus longitudes y latitudes.
def vincenty(lon1, lat1, lon2, lat2):
    #  Convierte las longitudes y latitudes de grados a radianes
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # Se define los parámetros del elipsoide WGS-84, que es un modelo matemático utilizado para representar la forma
    # de la Tierra. a es el radio ecuatorial, b es el radio polar y f es el achatamiento.
    a = 6378137.0
    b = 6356752.314245
    f = 1 / 298.257223563

    #  Se calcula la diferencia en longitud entre los dos puntos.
    L = lon2 - lon1
    #  Se calcula las latitudes reducidas de los dos puntos.
    U1 = atan((1 - f) * tan(lat1))
    U2 = atan((1 - f) * tan(lat2))
    # Se calcula los senos y cosenos de las latitudes reducidas.
    sinU1 = sin(U1)
    cosU1 = cos(U1)
    sinU2 = sin(U2)
    cosU2 = cos(U2)

    # Se Inicia la iteración de la fórmula de Vincenty para calcular la distancia entre los dos puntos.
    # lmbda se inicializa con el valor de L, que es la diferencia en longitud entre los dos puntos.
    lmbda = L
    # Inicia un bucle que se ejecutará hasta 100 veces. En cada iteración del bucle,
    # se actualizará el valor de lmbda utilizando la fórmula de Vincenty.
    for i in range(100):
        #  Se calcula el seno y el coseno de lmbda
        sinLambda = sin(lmbda)
        cosLambda = cos(lmbda)
        # Se calcula el valor de sinSigma
        sinSigma = sqrt((cosU2 * sinLambda) ** 2 + (cosU1 * sinU2 - sinU1 * cosU2 * cosLambda) ** 2)
        # Se  verifica si sinSigma es igual a cero. Si es así, la función devuelve cero como resultado.
        if sinSigma == 0:
            return 0
        # Se calcula los valores de cosSigma y sigma
        cosSigma = sinU1 * sinU2 + cosU1 * cosU2 * cosLambda
        sigma = atan2(sinSigma, cosSigma)
        # calculan los valores de sinAlpha y cosSqAlpha
        sinAlpha = cosU1 * cosU2 * sinLambda / sinSigma
        cosSqAlpha = 1 - sinAlpha ** 2
        # verifican si cosSqAlpha es diferente de cero. Si es así, se calcula el valor de cos2SigmaM
        # utilizando la fórmula dada. De lo contrario, se asigna cero a cos2SigmaM.
        if cosSqAlpha != 0:
            cos2SigmaM = cosSigma - 2 * sinU1 * sinU2 / cosSqAlpha
        else:
            cos2SigmaM = 0
        # Se calcula el valor de C.
        C = f / 16 * cosSqAlpha * (4 + f * (4 - 3 * cosSqAlpha))
        # Se guarda el valor anterior de lmbda en la variable lambda_prev
        lambda_prev = lmbda
        # Se actualiza el valor de lmbda utilizando la fórmula de Vincenty.
        lmbda = L + (1 - C) * f * sinAlpha * (sigma + C * sinSigma * (cos2SigmaM + C * cosSigma * (-1 + 2 * (cos2SigmaM ** 2))))
        #  verifican si la diferencia entre el valor actual y el valor anterior de lmbda es menor que un cierto umbral.
        #  Si es así, se sale del bucle.
        if abs(lmbda - lambda_prev) < 1e-12:
            break

    # calculan los valores finales de uSq, A, B, deltaSigma y s. El valor de s es la distancia entre los dos puntos en metros
    uSq = cosSqAlpha * (a ** 2 - b ** 2) / (b ** 2)
    A = 1 + uSq / 16384 * (4096 + uSq * (-768 + uSq * (320 - 175 * uSq)))
    B = uSq / 1024 * (256 + uSq * (-128 + uSq * (74 - 47 * uSq)))
    deltaSigma = B * sinSigma * (cos2SigmaM + B / 4 * (cosSigma * (-1 + 2 * (cos2SigmaM ** 2)) - B / 6 * cos2SigmaM * (-3 + 4 * (sinSigma ** 2)) * (-3 + 4 *(cos2SigmaM ** 2))))
    s = b * A *(sigma - deltaSigma)

    return s

    # Esta función convierte un objeto de tiempo en una cadena con el formato '%H:%M:%S'.
    # Si el argumento proporcionado no es un objeto de tiempo, la función devuelve el argumento sin modificarlo.
def convert_time_to_string(value):
    if isinstance(value, datetime.time):
        return value.strftime('%H:%M:%S')
    else:
        return value


def Limpieza(df="C:/Users/matia/OneDrive/Documents/portafolio/Ganaderia_de_presicion/dataSets/AA-P4-C364-5p.xls"):
    #El programa solo esta hecho para archivos csv y exel
    extension = os.path.splitext(df)[1]

    # Verificamos que tipo de documento tenemos que abrir para poder seleccionar la forma de leer el documento correcto
    if extension == '.csv':
        df = pd.read_csv(df, header=0, skiprows=6)
    elif extension in ['.xls', '.xlsx']:
        df = pd.read_excel(df, header=0, skiprows=6)
    else:
        print('El archivo no es ni csv ni Excel')

    #Elimina los espacios vacios de los datasets
    df = df.replace('\x00', '', regex=True)
    df.loc[:, 'Fecha'] = df['Fecha'].apply(lambda x: (np.nan if x == '' else x))
    df.loc[:, 'Fecha'] = df['Fecha'].apply(lambda x: (np.nan if x == ' ' else x))
    df.loc[:, 'Hora'] = df['Hora'].apply(lambda x: (np.nan if x == '' else x))
    df.loc[:, 'Temperatura_Ambiente'] = df['Temperatura_Ambiente'].apply(lambda x: (np.nan if x == '' else x))
    df.loc[:, 'Temperatura_Corporal'] = df['Temperatura_Corporal'].apply(lambda x: (np.nan if x == '' else x))
    df.loc[:, 'Humedad'] = df['Humedad'].apply(lambda x: (np.nan if x == '' else x))
    df.loc[:, 'Latitud'] = df['Latitud'].apply(lambda x: (np.nan if x == '' else x))
    df.loc[:, 'Longitud'] = df['Longitud'].apply(lambda x: (np.nan if x == '' else x))
    df.loc[:, 'Bateria'] = df['Bateria'].apply(lambda x: (np.nan if x == '' else x))
    df = df.dropna()

    #Eliminando los datos con errores del collar
    mask = ~df["Fecha"].str.startswith("0-")
    df = df[mask]
    mask = ~df["Hora"].str.startswith("-:")
    df = df[mask]

    #Convercion a tipos a los que pueda tratar el algoritmo
    df.loc[:, 'Hora'] = df['Hora'].apply(lambda x: datetime.strptime(x, '%H:%M').time() if isinstance(x, str) else x)
    df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d-%m-%y').dt.date
    df['Temperatura_Ambiente'] = df['Temperatura_Ambiente'].astype(float)
    df['Temperatura_Corporal'] = df['Temperatura_Corporal'].astype(float)
    df['Humedad'] = df['Humedad'].astype(float)
    df['Latitud'] = df['Latitud'].astype(float)
    df['Longitud'] = df['Longitud'].astype(float)
    df['Bateria'] = df['Bateria'].astype(float)

    # Conversion de los datos de geolocalizacion a estandares internacionales
    df.loc[:, "Latitud"] = df["Latitud"].apply(lambda x: (-x if x < 0 else x) * -0.000001)
    df.loc[:, "Longitud"] = df["Longitud"].apply(lambda x: (-x if x < 0 else x) * -0.000001)

    # Ordena el DataFrame por las columnas de fecha y hora
    #df = df.sort_values(by=['Fecha', 'Hora'], ascending=False)
    df = df.reset_index(drop=True)
    df.index = df.index + 1

    #Calculo de la distancia recorrida por el animal
    df.loc[:, "Distancia"] = [vincenty(lat1, lon1, lat2, lon2) for lat1, lon1, lat2, lon2 in zip(df['Latitud'], df['Longitud'], df['Latitud'].shift(), df['Longitud'].shift())]
    df.loc[1, "Distancia"] = 0.0
    df['FechaHora'] = pd.to_datetime(df['Fecha'].astype(str) + ' ' + df['Hora'].astype(str))

    # Calcular la diferencia de tiempo entre filas consecutivas
    df['time_diff'] = df['FechaHora'].diff()
    df['time_diff'] = df['time_diff'].fillna(pd.Timedelta(0))

    # Calcular la diferencia de distancia entre filas consecutivas
    df['distance_diff'] = df['Distancia'].diff()
    df['distance_diff'] = df['distance_diff'].fillna(0)

    # Calcular la diferencia de tiempo entre filas consecutivas en segundos
    df['time_diff_seconds'] = df['time_diff'].dt.total_seconds()

    # Calcular la velocidad
    df['Velocidad'] = (df['distance_diff'] / df['time_diff_seconds']).fillna(0)

    # convercion de m/s a km/h
    df['Velocidad'] = df['Velocidad'] * 3.6

    return df

# Funcion para mostrar solo los datos interesantes para el usuario
def muestra_datos_usuario(df):
    df_ui = df.loc[:,["Fecha", "Hora", "Temperatura_Ambiente", "Temperatura_Corporal", "Humedad", "Latitud", "Longitud", "Bateria", "Distancia", "Velocidad"]]
    return df_ui