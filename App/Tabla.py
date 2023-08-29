from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableView, QApplication
import TratamientoCSV
from ModelPandas import PandasModel

class Tabla(QWidget):
    def __init__(self, df):
        super().__init__()
        self.setWindowTitle("Tabla de datos")
        # Establecemos los tamaños de la ventana
        self.setMinimumSize(800, 600)
        self.setMaximumSize(1920, 1080)
        self.showMaximized()

        # Creamos un layout vertical para poner los botones en la parte superior de la pantalla
        vLayout = QVBoxLayout(self)
        # crea un nuevo objeto QTableView y lo asigna al atributo self.pandasTv.
        # Proporciona una vista de tabla para mostrar datos en una cuadrícula.
        self.pandasTv = QTableView(self)
        # Agrego el objeto QTableView al diseño vertical vLayout.
        vLayout.addWidget(self.pandasTv)
        # El método muestra_datos_usuario de la clase TratamientoCSV se utiliza para procesar el DataFrame antes de pasarlo al constructor del modelo.
        model = PandasModel(TratamientoCSV.muestra_datos_usuario(df))
        # Establece el modelo del objeto QTableView como el objeto PandasModel. Esto permite que la vista muestre los datos del DataFrame en una cuadrícula.
        self.pandasTv.setModel(model)
        #  Establece el color de fondo del objeto QTableView como gris
        self.pandasTv.setStyleSheet("background-color: lightgray;")
        # habilita la capacidad de ordenar los datos en la vista haciendo clic en los encabezados de las columnas.
        self.pandasTv.setSortingEnabled(True)

        # establece el diseño principal del widget
        self.setLayout(vLayout)

if __name__ == "__main__":
    app = QApplication([])
    window = QWidget()
    window.show()
    app.exec_()