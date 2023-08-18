import os
import tempfile

from PyQt5.QtCore import QUrl, QTranslator
from PyQt5.QtWidgets import QPushButton, QWidget, QHBoxLayout, QVBoxLayout, QComboBox
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QMessageBox, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import QtWebEngineWidgets
import folium
from folium import plugins
from platformdirs import windows

import TratamientoCSV
import Tabla
import Grafico


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initWindow()

    def initWindow(self):
        self.setWindowTitle(self.tr("Ganaderia de Precisión"))
        self.showMaximized()
        self.setMinimumSize(1280, 800)
        self.setMaximumSize(1920, 1080)
        self.setWindowState(Qt.WindowMaximized)
        self.setWindowFlags(Qt.Window)
        self.buttonUI()

    def buttonUI(self):

        open_act = QAction(QIcon("open.png"), "Abrir", self)
        open_act.setShortcut("Ctrl+O")
        open_act.triggered.connect(self.abrir_archivos)

        save_act = QAction(QIcon("save.png"), "Guardar", self)
        save_act.setShortcut("Ctrl+S")
        save_act.triggered.connect(self.save_map)

        close_act = QAction(QIcon("close.png"), "Cerrar", self)
        close_act.setShortcut("Ctrl+Q")
        close_act.triggered.connect(self.close)

        about_act = QAction(QIcon("about.png"), "Ayuda", self)
        about_act.triggered.connect(self.about_dialog)

        menu_bar = self.menuBar()
        # menu_bar.setNativeMenuBar(False)
        file_menu = menu_bar.addMenu("Archivo")
        file_menu.addAction(open_act)
        file_menu.addAction(save_act)
        file_menu.addSeparator()
        file_menu.addAction(close_act)

        edit_menu = menu_bar.addMenu("Edicion")

        tools_menu = menu_bar.addMenu("Herramientas")

        help_menu = menu_bar.addMenu("Ayuda")
        help_menu.addAction(about_act)

        # Creacion de botones
        self.btn_abrir = QPushButton("Abrir nuevo", self)
        self.btn_abrir.setFixedSize(120, 50)
        self.btn_abrir.setIcon(QIcon("./png/folder.png"))
        self.btn_abrir.clicked.connect(self.abrir_archivos)

        # Boton rotar 180
        self.btn_tabla = QPushButton("Mostrar Tablas", self)
        self.btn_tabla.setFixedSize(120, 50)
        self.btn_tabla.setIcon(QIcon("./png/table.png"))
        self.btn_tabla.clicked.connect(self.ver_tabla)

        # Boton rotar Horizontal
        self.btn_grafico = QPushButton("Ver Graficos", self)
        self.btn_grafico.setFixedSize(120, 50)
        self.btn_grafico.setIcon(QIcon("./png/stadistic.png"))
        self.btn_grafico.clicked.connect(self.ver_grafico)

        # Boton Cambiar mapa
        self.cobox_mapa = QComboBox(self)
        self.cobox_mapa.addItems(["Heap Map", "Marcadores"])
        self.cobox_mapa.setFixedSize(120, 50)
        self.btn_ok = QPushButton("Ok", self)
        self.btn_ok.setFixedSize(120, 50)
        self.btn_ok.setIcon(QIcon("./png/rotate.png.png"))
        self.btn_ok.clicked.connect(self.cambiar_mapa)

        # Boton salir
        self.btn_exit = QPushButton("Salir", self)
        self.btn_exit.setFixedSize(120, 50)
        self.btn_exit.setIcon(QIcon("./png/close.png"))
        self.btn_exit.clicked.connect(self.close)

        self.view = QtWebEngineWidgets.QWebEngineView()
        self.view.setContentsMargins(50, 50, 50, 50)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        lay = QHBoxLayout(central_widget)

        button_container = QWidget()
        vlay = QVBoxLayout(button_container)
        vlay.setSpacing(20)
        vlay.addStretch()
        vlay.addWidget(self.btn_abrir)
        vlay.addWidget(self.btn_tabla)
        vlay.addWidget(self.btn_grafico)
        vlay.addWidget(self.cobox_mapa)
        vlay.addWidget(self.btn_ok)
        vlay.addWidget(self.btn_exit)
        vlay.addStretch()
        lay.addWidget(button_container)
        lay.addWidget(self.view, stretch=1)

        # name, ext = QFileDialog.getOpenFileName(self, "Abrir Archivo", "", "CSV (*.csv);; Exel (*.xls)")
        self.df = TratamientoCSV.Limpieza()

        mapa = self.mostrar_head_map()

        _, temp_map_file = tempfile.mkstemp(suffix='.html')
        mapa.save(temp_map_file)
        self.view.load(QUrl.fromLocalFile(os.path.abspath(temp_map_file)))

    def abrir_archivos(self):
        try:
            nombre, _ = QFileDialog.getOpenFileName(self, "Abrir Documento", "", "Exel (*.xls);; CSV (*.csv)")
            if nombre:
                self.df = TratamientoCSV.Limpieza(nombre)
                self.cambiar_mapa()
            else:
                QMessageBox(self, "Error", "No se pudo abrir el archivo", QMessageBox.Ok)
        except FileNotFoundError:
            print("Archivo no seleccionado")

    def cambiar_mapa(self):
        try:
            if self.cobox_mapa.currentText() == "Heap Map":
                mapa = self.mostrar_head_map()
                _, temp_map_file = tempfile.mkstemp(suffix='.html')
                mapa.save(temp_map_file)
                self.view.load(QUrl.fromLocalFile(os.path.abspath(temp_map_file)))
            else:
                mapa = self.mostrar_marcadores()
                _, temp_map_file = tempfile.mkstemp(suffix='.html')
                mapa.save(temp_map_file)
                self.view.load(QUrl.fromLocalFile(os.path.abspath(temp_map_file)))
        except:
            QMessageBox.information(self, "Error", "")

    def ver_tabla(self):
        self.new_tabla = Tabla.Tabla(self.df)
        self.new_tabla.show()

    def ver_grafico(self):
        self.new_grafico = Grafico.Aplicacion(self.df)
        self.new_grafico.show()

    def mostrar_marcadores(self):
        self.df['cantidad'] = self.df.groupby(['Latitud', 'Longitud'])['Latitud'].transform('count')

        mapa = folium.Map(location=[self.df['Latitud'].mean(), self.df['Longitud'].mean()], zoom_start=13, prefer_canvas=True)

        folium.TileLayer(tiles='https://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', attr='Google',
                         name='Google Satellite', max_zoom=20,
                         subdomains=['mt0', 'mt1', 'mt2', 'mt3']).add_to(mapa)

        # Añadir marcadores para cada ubicación
        for i, row in self.df.iterrows():
            folium.Marker([row['Latitud'], row['Longitud']],
                          popup=f"Humedad: {row['Humedad']:.2f}\nFecha: {row['Fecha']} {row['Hora']}\n").add_to(
                mapa)

        return mapa

    def mostrar_head_map(self):
        ubicaciones = self.df[['Latitud', 'Longitud']]
        self.df['Latitud'] = self.df['Latitud'].astype(float)
        self.df['Longitud'] = self.df['Longitud'].astype(float)
        url = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'
        attr = 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
        mapa = folium.Map(location=[self.df["Latitud"].mean(), self.df["Longitud"].mean()], zoom_start=12,
                          control_scale=True, prefer_canvas=True)
        folium.TileLayer(tiles=url, attr=attr).add_to(mapa)
        plugins.MarkerCluster(ubicaciones).add_to(mapa)
        mapa.add_child(plugins.HeatMap(ubicaciones, radius=15))
        for index, location_info in self.df.iterrows():
            lat = location_info["Latitud"]
            lon = location_info["Longitud"]
            popup = 'Temperatura ambiente:  <b>' + str(
                location_info["Temperatura_Ambiente"]) + '</b></br>Temperatura corporal: <b>' + str(
                location_info["Temperatura_Corporal"]) + '</b>'
            folium.CircleMarker(location=[lat, lon], radius=2, popup=folium.Popup(popup, max_width=200)).add_to(mapa)
        minimap = plugins.MiniMap(toggle_display=True)
        mapa.add_child(minimap)
        return mapa

    def save_map(self):
        pass

    def open_act(self):
        pass

    def about_dialog(self):
        QMessageBox.about(self,"Acerca de ganaderia de presiciòn", "Podrian pagarle al informatico para que termine che")

if __name__ == "__main__":
    app = QApplication([])
    translator = QTranslator()
    if translator.load("es.qm"):
        app.installTranslator(translator)
    window = MainWindow()
    window.show()
    app.exec_()