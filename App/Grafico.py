import numpy as np
import seaborn as sns
from PyQt5.QtGui import QIcon

import TratamientoCSV

import matplotlib.pyplot as plt
import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QFrame, QComboBox, QPushButton, QMessageBox, \
    QSpacerItem, QSizePolicy, QHBoxLayout, QWidget


class Grafica_Temp_c_a(FigureCanvasQTAgg):
    def __init__(self,df):
        figure = plt.figure()
        super(Grafica_Temp_c_a, self).__init__(figure)
        self.grafica = figure.add_subplot(111)
        self.grafica.scatter(df['Temperatura_Ambiente'], df['Temperatura_Corporal'], color='red', marker='o')

        # Ajustar una línea de tendencia
        z = np.polyfit(df['Temperatura_Ambiente'], df['Temperatura_Corporal'], 1)
        p = np.poly1d(z)
        self.grafica.plot(df['Temperatura_Ambiente'], p(df['Temperatura_Ambiente']), 'k--')

        # Agregar etiquetas y título
        self.grafica.set_xlabel('Temperatura ambiente')
        self.grafica.set_ylabel('Temperatura del animal')
        self.grafica.set_title('Temperatura del animal en función de la temperatura ambiente')


class Grafica_Temp_c_a_m(FigureCanvasQTAgg):
    def __init__(self, df):
        # Crear una figura
        figure = plt.figure()

        # Llamar al constructor de la clase base con la figura como argumento
        super().__init__(figure)

        # Crear un objeto de ejes
        ejes = figure.add_subplot(111)

        # Dibujar los datos en los ejes
        y2 = df["Temperatura_Ambiente"]
        y1 = df["Temperatura_Corporal"]
        x = (y2 + y1) / 2
        ejes.plot(x, y1, "or--", label='Temperatura Ambiente Promedio')
        ejes.plot(x, y2, "ob--", label='Temperatura Corporal Promedio')

        # Agregar etiquetas y título
        ejes.set_ylabel("Temperatura promedio")
        ejes.set_xlabel("Día")
        ejes.ticklabel_format(axis='y', style='plain', scilimits=(0, 0), useOffset=False, useLocale=None,
                              useMathText=None)
        ejes.set_title("Temperatura ambiente y corporal promedio diara")
        ejes.legend()


class Grafica_Temp_c_a_bpa(FigureCanvasQTAgg):
    def __init__(self, df):
        # Crear una figura
        figure = plt.figure()

        # Llamar al constructor de la clase base con la figura como argumento
        super().__init__(figure)

        # Crear un objeto de ejes
        ejes = figure.add_subplot(111)

        # Dibujar los datos en los ejes
        x = df['Fecha'].dt.strftime('%d/%m/%Y')
        y = df["Temperatura_Ambiente"]
        sns.boxplot(x=x, y=y, width=0.5, ax=ejes)
        sns.stripplot(x=x, y=y, data=df, size=4, color=".3", linewidth=0, ax=ejes)

        # Agregar etiquetas y título
        ejes.set_ylabel("Temperatura Ambiente")
        ejes.set_xlabel("Fecha")
        ejes.set_title("Temperatura Ambiente por Fecha")

class Grafica_Temp_c_a_bpc(FigureCanvasQTAgg):
    def __init__(self, df):
        # Crear una figura
        figure = plt.figure()

        # Llamar al constructor de la clase base con la figura como argumento
        super().__init__(figure)

        # Crear un objeto de ejes
        ejes = figure.add_subplot(111)

        x = df['Fecha'].dt.strftime('%d/%m/%Y')
        y = df["Temperatura_Corporal"]
        sns.boxplot(x=x, y=y, width=0.5)
        sns.stripplot(x=x, y=y, data=df, size=4, color=".3", linewidth=0)
        ejes.set_ylabel("Temperatura Corporal")
        ejes.set_xlabel("Fecha")
        ejes.set_title("Temperatura Corporal por Fecha")


class Aplicacion(QMainWindow):
    def __init__(self,df=TratamientoCSV.Limpieza()):
        super(Aplicacion, self).__init__()

        self.df = df
        self.setMinimumSize(800, 600)
        self.setMaximumSize(1920, 1080)
        self.showMaximized()

        self.grafico = Grafica_Temp_c_a(df)

        # Boton Cambiar grafico
        self.cobox_grafico = QComboBox(self)
        self.cobox_grafico.addItems(["Temperatura Amb/Corporal regresión", "Temperatura Amb/Corporal promedio diario",
                                     "Temperatura Ambiente box plot", "Temperatura Corporal box plot"])
        self.cobox_grafico.setFixedSize(300, 50)
        self.cobox_grafico.currentIndexChanged.connect(self.actualizar_grafico)
        self.grafico.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)

        # Creando objeto de la barra de navegacion
        barra_navegacion = NavigationToolbar2QT(self.grafico, self)

        # Crear un contenedor para la barra de navegación y el combobox
        contenedor_barra = QWidget()
        layout_barra = QHBoxLayout()
        layout_barra.addWidget(barra_navegacion)
        layout_barra.addWidget(self.cobox_grafico)
        contenedor_barra.setLayout(layout_barra)
        contenedor_barra.setMaximumHeight(60)

        #Agregando el diseño
        self.vlyt = QVBoxLayout()
        self.vlyt.addWidget(contenedor_barra)
        # Agregar el gráfico al diseño
        self.vlyt.addWidget(self.grafico)

        #Agregando diseño al contenedor
        contenedor = QFrame()
        contenedor.setLayout(self.vlyt)

        self.setCentralWidget(contenedor)

    def actualizar_grafico(self):
        seleccion = self.cobox_grafico.currentText()
        if seleccion == "Temperatura Amb/Corporal regresión":
            # Crear una nueva instancia de la clase Grafica_Temp_c_a
            nuevo_grafico = Grafica_Temp_c_a(self.df)

            # Reemplazar el gráfico actual por el nuevo gráfico
            self.grafico.setParent(None)
            self.grafico = nuevo_grafico
            self.vlyt.insertWidget(1, self.grafico)
        elif seleccion == "Temperatura Amb/Corporal promedio diario":
            # Crear una nueva instancia de la clase Grafica_Temp_c_a
            nuevo_grafico = Grafica_Temp_c_a_m(self.df)

            # Reemplazar el gráfico actual por el nuevo gráfico
            self.grafico.setParent(None)
            self.grafico = nuevo_grafico
            self.vlyt.insertWidget(1, self.grafico)
        elif seleccion == "Temperatura Ambiente box plot":
            # Crear una nueva instancia de la clase Grafica_Temp_c_a
            nuevo_grafico = Grafica_Temp_c_a_bpa(self.df)

            # Reemplazar el gráfico actual por el nuevo gráfico
            self.grafico.setParent(None)
            self.grafico = nuevo_grafico
            self.vlyt.insertWidget(1, self.grafico)
        elif seleccion == "Temperatura Corporal box plot":
            # Crear una nueva instancia de la clase Grafica_Temp_c_a
            nuevo_grafico = Grafica_Temp_c_a_bpc(self.df)

            # Reemplazar el gráfico actual por el nuevo gráfico
            self.grafico.setParent(None)
            self.grafico = nuevo_grafico
            self.vlyt.insertWidget(1, self.grafico)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Aplicacion()
    window.show()
    sys.exit(app.exec_())