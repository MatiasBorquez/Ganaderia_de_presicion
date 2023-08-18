from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableView
import TratamientoCSV
from ModelPandas import PandasModel


class Tabla(QWidget):
    def __init__(self, df):
        super().__init__()
        self.setWindowTitle("Tabla de datos")
        self.setMinimumSize(800, 600)
        self.setMaximumSize(1920, 1080)
        self.showMaximized()

        vLayout = QVBoxLayout(self)
        self.pandasTv = QTableView(self)
        vLayout.addWidget(self.pandasTv)
        model = PandasModel(TratamientoCSV.muestra_datos_usuario(df))
        self.pandasTv.setModel(model)
        self.pandasTv.setSortingEnabled(True)

        self.setLayout(vLayout)