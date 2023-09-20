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

import TratamientoCSV
import Tabla
import Grafico

estilo ="""
QWidget{
background-color: rgb(50, 50, 50);
}
QWidget#orden_widget{
border: 3px solid white;
}
QLabel#titulo{
color: white;
}
QPushButton{
background-color: rgb(200, 200, 200);
border: 2px solid white;
border-radius: 15px;
padding: 5px;
color: black;
}
QPushButton:hover{
background-color: rgb(255, 255, 255);
}
QPushButton:pressed{
background: white;
}
QGroupBox{
color: black;
font-weight: bold;
font-size: 15px;
}
QMenuBar{
background-color: rgb(200, 200, 200);
border: 2px solid white;
padding: 5px;
color: black;
}
QMenuBar:pressed{
background: white;
}
QMenu::item:selected {
background-color: white;
}
QComboBox {
    background-color: rgb(250, 250, 250);
    border: 2px solid white;
    border-radius: 10px;
    padding: 5px;
    color: black;
}
QComboBox::down-arrow {
    width: 5px;
    height: 5px;
    top: 2px;
    right: 2px;
}
QComboBox QAbstractItemView {
    background-color: rgb(250, 250, 250);
    color: rgb(0, 0, 0);
    selection-background-color: rgb(150, 150, 150);
    selection-color: rgb(255, 255, 255);
}
QMessageBox{
background-color: rgb(200, 200, 200);
}
QMessageBox QLabel {
color: rgb(0, 0, 0);
background-color: rgb(200, 200, 200);
}
"""

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initWindow()

    # Inicializacion de la ventana
    def initWindow(self):
        self.setWindowTitle(self.tr("Ganaderia de Precisión"))
        self.showMaximized()
        self.setMinimumSize(1280, 800)
        self.setMaximumSize(1920, 1080)
        # Establece la ventana en la maxima extencion
        self.setWindowState(Qt.WindowMaximized)
        #  Qt.Window es una bandera de tipo que especifica que el widget es una ventana de nivel superior
        self.setWindowFlags(Qt.Window)
        self.UI()

    def UI(self):
        # barra de menu superior

        # Crea boton para abrir un nuevo archivo
        open_act = QAction(QIcon("open.png"), "Abrir", self)
        open_act.setShortcut("Ctrl+O")
        open_act.triggered.connect(self.abrir_archivos)

        # Crea boton para guardar el mapa actual
        save_act = QAction(QIcon("save.png"), "Guardar", self)
        save_act.setShortcut("Ctrl+S")
        save_act.triggered.connect(self.save_map)

        # Crea boton para cerrar la la aplicacion
        close_act = QAction(QIcon("close.png"), "Cerrar", self)
        close_act.setShortcut("Ctrl+Q")
        close_act.triggered.connect(self.close)

        # Crea boton de ayuda
        about_act = QAction(QIcon("about.png"), "Ayuda", self)
        about_act.triggered.connect(self.about_dialog)

        # Creacion del menu bar
        menu_bar = self.menuBar()
        # menu_bar.setNativeMenuBar(False)
        file_menu = menu_bar.addMenu("Archivo")
        # agregar los botones dentro del menu bar
        file_menu.addAction(open_act)
        file_menu.addAction(save_act)
        file_menu.addSeparator()
        file_menu.addAction(close_act)

        edit_menu = menu_bar.addMenu("Edicion")

        tools_menu = menu_bar.addMenu("Herramientas")

        help_menu = menu_bar.addMenu("Ayuda")
        help_menu.addAction(about_act)

        # Creacion de botones
        self.btn_abrir = QPushButton("Abrir uno", self)
        self.btn_abrir.setFixedSize(120, 50)
        self.btn_abrir.setIcon(QIcon("./png/folder.png"))
        self.btn_abrir.clicked.connect(self.abrir_archivo)

        self.btn_abrir_varios = QPushButton("Abrir varios", self)
        self.btn_abrir_varios.setFixedSize(120, 50)
        self.btn_abrir_varios.setIcon(QIcon("./png/folder.png"))
        self.btn_abrir_varios.clicked.connect(self.abrir_archivos)

        # Boton Para Mostrar todos los datos
        self.btn_tabla = QPushButton("Mostrar Datos", self)
        self.btn_tabla.setFixedSize(120, 50)
        self.btn_tabla.setIcon(QIcon("./png/table.png"))
        self.btn_tabla.clicked.connect(self.ver_tabla)

        # Boton Para graficos
        self.btn_grafico = QPushButton("Ver Graficos", self)
        self.btn_grafico.setFixedSize(120, 50)
        self.btn_grafico.setIcon(QIcon("./png/stadistic.png"))
        self.btn_grafico.clicked.connect(self.ver_grafico)

        # Boton Cambiar mapa
        self.cobox_mapa = QComboBox(self)
        self.cobox_mapa.setSizeAdjustPolicy(QComboBox.AdjustToContents)
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

        # QWebEngineView se utiliza para mostrar el mapa del folium
        self.view = QtWebEngineWidgets.QWebEngineView()
        self.view.setContentsMargins(50, 50, 50, 50)

        # se crea un widget central y se establece como el widget central de la ventana principal.
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        lay = QHBoxLayout(central_widget)

        # Se crea un contenedor de botones y se agrega un diseño vertical al contenedor de botones.
        button_container = QWidget()
        vlay = QVBoxLayout(button_container)
        # El diseño vertical se le establece un espaciado de 20 píxeles entre los elementos
        vlay.setSpacing(20)
        # Se agrega un estiramiento al principio y al final del diseño vertical para empujar los widgets hacia el centro.
        vlay.addStretch()
        # se agregan los botones y un cuadro combinado al diseño vertical.
        vlay.addWidget(self.btn_abrir)
        vlay.addWidget(self.btn_abrir_varios)
        vlay.addWidget(self.btn_tabla)
        vlay.addWidget(self.btn_grafico)
        vlay.addWidget(self.cobox_mapa)
        vlay.addWidget(self.btn_ok)
        vlay.addWidget(self.btn_exit)
        vlay.addStretch()
        # El contenedor de botones se agrega al diseño horizontal.
        lay.addWidget(button_container)
        lay.addWidget(self.view, stretch=1)

        # name, ext = QFileDialog.getOpenFileName(self, "Abrir Archivo", "", "CSV (*.csv);; Exel (*.xls)")
        # Se llama a la funcion que va a trata los datos a mostrarse por defecto
        self.df = TratamientoCSV.Limpieza()

        # Llamo a la funcion que crear head map y lo guardo en la variable mapa
        mapa = self.crear_head_map()

        #  crea un archivo temporal con la extensión .html
        _, temp_map_file = tempfile.mkstemp(suffix='.html')
        # guarda el mapa en el archivo temporal utilizando el método save() del objeto.
        mapa.save(temp_map_file)
        #  abre el archivo temporal en modo de lectura y escritura y lee su contenido en una variable html
        with open(temp_map_file, 'r+') as f:
            html = f.read()
            # reemplaza la etiqueta <head> con una etiqueta <head> que contiene una etiqueta <style> para agregar estilos CSS al contenido HTML
            html = html.replace('<head>',
                                '<head><style>body {border: px solid gray; border-radius: 15px; padding: 10px; color: black;}</style>')
            # mueve el puntero del archivo al principio del archivo y escribe el contenido modificado de html en el archivo
            f.seek(0)
            f.write(html)
            #  trunca el archivo para eliminar cualquier contenido adicional y carga el archivo temporal en una vista QWebEngineView
            #  utilizando el método load() y la clase QUrl.fromLocalFile()
            f.truncate()
        self.view.load(QUrl.fromLocalFile(os.path.abspath(temp_map_file)))

    # Funcion para abrir los el archivo a tratar
    def abrir_archivo(self):
        try:
            # Abre un cuadro de dialogo donde el usuario va a podes seleccionar el archivo de interes, ya sea exel o csv
            nombre, _ = QFileDialog.getOpenFileName(self, "Abrir Documento", "", "Exel (*.xls);; CSV (*.csv)")
            # Verifica si se devuelve un archivo o no se selecciono nada
            if nombre:
                # Llama a la funcion que tratara los datos para poderlos mostrar
                self.df = TratamientoCSV.Limpieza(nombre)
                # Mostramos el nuevo mapa
                self.cambiar_mapa()
            else:
                QMessageBox.critical(self, "Error", "No se pudo abrir el archivo")
        except FileNotFoundError:
            QMessageBox.critical(self, "Error", "Error en proceso de abrir Archivo")

    def abrir_archivos(self):
        try:
            # Abre un cuadro de dialogo donde el usuario va a podes seleccionar el archivo de interes, ya sea exel o csv
            nombres, _ = QFileDialog.getOpenFileNames(self, "Abrir Documento", "", "Exel (*.xls);; CSV (*.csv)")
            if nombres:
                for nombre in nombres:
                    print(nombre)
            # Verifica si se devuelve un archivo o no se selecciono nada
            if nombre:
                # Llama a la funcion que tratara los datos para poderlos mostrar
                self.df = TratamientoCSV.Limpieza(nombre)
                # Mostramos el nuevo mapa
                self.cambiar_mapa()
            else:
                QMessageBox.critical(self, "Error", "No se pudo abrir el archivo")
        except FileNotFoundError:
            QMessageBox.critical(self, "Error", "Error en proceso de abrir Archivo")

    # cambia el mapa mostrado en una vista QWebEngineView
    def cambiar_mapa(self):
        try:
            # verifica el texto actual del cobox_mapa, si es Head Map y se va al else si es marcadores
            if self.cobox_mapa.currentText() == "Heap Map":
                # Crea nuevo mapa head map
                mapa = self.crear_head_map()
                # Guarda mapa en una extencion temporal html
                _, temp_map_file = tempfile.mkstemp(suffix='.html')
                mapa.save(temp_map_file)
                #  abre el archivo temporal en modo de lectura y escritura y lee su contenido en una variable html
                with open(temp_map_file, 'r+') as f:
                    html = f.read()
                    # reemplaza la etiqueta <head> con una etiqueta <head> que contiene una etiqueta <style> para agregar estilos CSS al contenido HTML
                    html = html.replace('<head>',
                                        '<head><style>body {border: px solid gray; border-radius: 15px; padding: 10px; color: black;}</style>')
                    # mueve el puntero del archivo al principio del archivo y escribe el contenido modificado de html en el archivo
                    f.seek(0)
                    f.write(html)
                    #  trunca el archivo para eliminar cualquier contenido adicional y carga el archivo temporal en una vista QWebEngineView
                    #  utilizando el método load() y la clase QUrl.fromLocalFile()
                    f.truncate()
                self.view.load(QUrl.fromLocalFile(os.path.abspath(temp_map_file)))

            else:
                # Crea nuevo mapa marcadores
                mapa = self.crear_marcadores()
                # Guarda mapa en una extencion temporal html
                _, temp_map_file = tempfile.mkstemp(suffix='.html')
                mapa.save(temp_map_file)
                #  abre el archivo temporal en modo de lectura y escritura y lee su contenido en una variable html
                with open(temp_map_file, 'r+') as f:
                    html = f.read()
                    # reemplaza la etiqueta <head> con una etiqueta <head> que contiene una etiqueta <style> para agregar estilos CSS al contenido HTML
                    html = html.replace('<head>',
                                        '<head><style>body {border: px solid gray; border-radius: 15px; padding: 10px; color: black;}</style>')
                    # mueve el puntero del archivo al principio del archivo y escribe el contenido modificado de html en el archivo
                    f.seek(0)
                    f.write(html)
                    #  trunca el archivo para eliminar cualquier contenido adicional y carga el archivo temporal en una vista QWebEngineView
                    #  utilizando el método load() y la clase QUrl.fromLocalFile()
                    f.truncate()
                self.view.load(QUrl.fromLocalFile(os.path.abspath(temp_map_file)))
        except:
            QMessageBox.information(self, "Error", "")

    def ver_tabla(self):
        # Crea una nueva tabla de datos
        self.new_tabla = Tabla.Tabla(self.df)
        # Muestra en una nueva ventana
        self.new_tabla.show()

    def ver_grafico(self):
        # Crea una nueva ventana de graficos
        self.new_grafico = Grafico.Aplicacion(self.df)
        self.new_grafico.show()

    # Funcion para crear una mapa de marcadores de la localizacion del animal
    def crear_marcadores(self):
        # Creo una nueva columna cantidad al dataframe que contiene el recuento de filas agrupadas por las columnas latitud y longitud
        self.df['cantidad'] = self.df.groupby(['Latitud', 'Longitud'])['Latitud'].transform('count')
        # creo un objeto de mapa centrado en la media de las coordenadas de latitud y longitud del dataframe y con un nivel de zoom inicial de 13.
        mapa = folium.Map(location=[self.df['Latitud'].mean(), self.df['Longitud'].mean()], zoom_start=13, prefer_canvas=True)
        # Se agrega una capa de mosaico de "google satellite" al mapa utilizando la clase folium.TileLayer
        folium.TileLayer(tiles='https://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', attr='Google',
                         name='Google Satellite', max_zoom=20,
                         subdomains=['mt0', 'mt1', 'mt2', 'mt3']).add_to(mapa)

        # Añadir marcadores para cada ubicación, mediante un bucle
        for i, row in self.df.iterrows():
            folium.Marker([row['Latitud'], row['Longitud']],
                          popup=f"Humedad: {row['Humedad']:.2f}\nFecha: {row['Fecha']} {row['Hora']}\n").add_to(mapa)
        # Regresa el objeto mapa
        return mapa

    def crear_head_map(self):
        # elecciono las columnas latitud y longitud del dataframe y las almacena en una variable llamada ubicaciones
        ubicaciones = self.df[['Latitud', 'Longitud']]
        # convierto las columnas latitud y longitud a tipo flotante
        self.df['Latitud'] = self.df['Latitud'].astype(float)
        self.df['Longitud'] = self.df['Longitud'].astype(float)
        # defino una URL
        url = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'
        # defino un atributo para una capa de mosaico de Esri World Imagery
        attr = 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
        # creo un objeto de mapa centrado en la media de las coordenadas de latitud y longitud del DataFrame y con un nivel de zoom inicial de 12
        mapa = folium.Map(location=[self.df["Latitud"].mean(), self.df["Longitud"].mean()], zoom_start=12,
                          control_scale=True, prefer_canvas=True)
        # agrego la capa de mosaico al mapa utilizando la clase folium.TileLayer
        folium.TileLayer(tiles=url, attr=attr).add_to(mapa)
        # agrego un grupo de marcadores al mapa utilizando la clase plugins.MarkerCluster y se pasa la variable ubicaciones como argumento
        plugins.MarkerCluster(ubicaciones).add_to(mapa)
        # agrego un mapa de calor al mapa utilizando la clase plugins.HeatMap y se pasa la variable ubicaciones como argumento con un radio de 15
        mapa.add_child(plugins.HeatMap(ubicaciones, radius=15))
        # se itera sobre cada fila del dataframe y se agrega un marcador circular al mapa en la ubicación especificada por las coordenadas de latitud y longitud de la fila
        for index, location_info in self.df.iterrows():
            lat = location_info["Latitud"]
            lon = location_info["Longitud"]
            #  El marcador tiene un elemento emergente que muestra la temperatura ambiente y corporal de la fila
            popup = 'Temperatura ambiente:  <b>' + str(
                location_info["Temperatura_Ambiente"]) + '</b></br>Temperatura corporal: <b>' + str(
                location_info["Temperatura_Corporal"]) + '</b>'
            folium.CircleMarker(location=[lat, lon], radius=2, popup=folium.Popup(popup, max_width=200)).add_to(mapa)
        # agrego un minimapa al mapa utilizando la clase plugins.MiniMap con una opción para alternar su visualización y se devuelve el objeto de mapa
        minimap = plugins.MiniMap(toggle_display=True)
        mapa.add_child(minimap)
        #  Regresa el objeto mapa
        return mapa

    def save_map(self):
        pass

    def open_act(self):
        pass

    def about_dialog(self):
        QMessageBox.about(self,"Acerca de ganaderia de presiciòn", "En futuras actualizaciones estara disponible")

if __name__ == "__main__":
    app = QApplication([])
    app.setStyleSheet(estilo)
    translator = QTranslator()
    if translator.load("es.qm"):
        app.installTranslator(translator)
    window = MainWindow()
    window.show()
    app.exec_()